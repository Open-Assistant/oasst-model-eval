import os
import json
import argparse
import time
import datetime

import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def parse_args():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Enter message into URL')
    parser.add_argument('--url', type=str, default="https://chat.lmsys.org/", help='URL to open')
    parser.add_argument('--model', type=str, default="vicuna", help='Model to use')
    parser.add_argument('--input_file', type=str, default="data/prompt_lottery_en_250_text.jsonl", help='Path to input file')
    parser.add_argument('--num_samples', type=int, default=1, help='Number of samples to generate')
    parser.add_argument('--chrome_driver_path', type=str, default="/usr/local/bin/chromedriver", help='Path to Chrome driver')
    parser.add_argument('--verbose', type=bool, default=True, help='Print output')

    # Parse arguments
    args = parser.parse_args()
    return args

def read_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
        objs = [json.loads(line) for line in lines]
    return objs

def get_response_text(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, '.message.bot > *')
    texts = []
    for element in elements:
        text = element.text
        if text:
            texts.append(text)
    return "\n\n".join(texts)

def get_response(driver, message):
    # Wait until target element is loaded
    wait = WebDriverWait(driver, 20)
    target_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/gradio-app/div/div/div/div/div/div[4]/div[1]/div/div/label/textarea')))

    time.sleep(1)

    # Paste message into textarea
    target_element.clear()
    target_element.click()
    for char in message:
        if char == "\n":
            target_element.send_keys(Keys.SHIFT + Keys.ENTER)
        else:
            target_element.send_keys(char)
    target_element.send_keys(Keys.ENTER)

    time.sleep(1)

    # Wait until the message is completed
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.message.bot p')))

    start_time = time.time()
    generating = True
    while generating:
        if time.time() - start_time > 120:
            raise TimeoutError("Timed out waiting for response")
        try:
            text_now = get_response_text(driver)
            if "▌" in text_now:
                time.sleep(1)
                continue
            time.sleep(1)
            text_later = get_response_text(driver)
            if "▌" in text_later or text_now != text_later:
                time.sleep(1)
                continue
            generating = False
        except:
            pass
    response = get_response_text(driver)

    # Reset history
    reset_button = driver.find_element(By.XPATH, '//*[@id="component-17"]')
    reset_button.click()
    time.sleep(1)

    return response


def select_model(driver, model_name):
    wait = WebDriverWait(driver, 20)

    if model_name.lower() == "alpaca":
        # Click on the dropdown element
        dropdown_element = wait.until(EC.element_to_be_clickable((By.XPATH,  '/html/body/gradio-app/div/div/div/div/div/div[2]/div/label/div/div[1]')))
        time.sleep(0.5)
        dropdown_element.click()

        # Wait for the "alpaca" model option to be clickable and click it
        alpaca_model_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="component-4"]/label/div/ul/li[3]')))
        time.sleep(0.5)
        alpaca_model_option.click()
    elif model_name.lower() == "vicuna":
        pass
    else:
        raise ValueError(f"Invalid model name: {model_name}")


def main(args):
    # Read input file
    prompts = read_input(args.input_file)

    output_file = f"{datetime.datetime.now().strftime('%Y-%m-%d')}_{args.model}_sample.jsonl"

    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            sampling_report = json.load(f)

        results = sampling_report["prompts"]
    else:
        results = []
        sampling_report = {
            "model_name": args.model,
            "date": datetime.datetime.now().isoformat(),
            "args": args.__dict__,
            "prompts": results,
        }

    if len(results) > 0:
        already_completed_prompts = set(result["prompt"] for result in results)
        prompts = [prompt for prompt in prompts if prompt not in already_completed_prompts]

        sampling_config = results[0]["results"][0]["sampling_config"]
        sampling_params = results[0]["results"][0]["sampling_params"]
    else:
        sampling_config = "sample"
        sampling_params = {
            "max_new_tokens": 512,
            "min_new_tokens": 0,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 1.0,
        }


    # Open browser
    driver = webdriver.Chrome(args.chrome_driver_path)
    driver.get(args.url)

    wait = WebDriverWait(driver, 20)
    for i in range(5):
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/gradio-app/div/div/div/div/div/div[4]/div[1]/div/div/label/textarea')))
            break
        except:
            driver.refresh()
    time.sleep(5)

    select_model(driver, args.model)

    try:
        for prompt in tqdm.tqdm(prompts, smoothing=0.0):
            outputs = []
            for i in range(args.num_samples):
                response = None
                for _ in range(2):
                    try:
                        response = get_response(driver, prompt)
                        break
                    except Exception as e:
                        print(e)
                        print("Retrying...")
                        continue
                if response is None:
                    print(f'Failed to get response for prompt "{prompt}"')
                    response = "Failed to get response (probably violates content policy)"
                outputs.append(response)

                if args.verbose:
                    print(f"===[ Config: {sampling_config} [{i+1}/{args.num_samples}] ]===\n")
                    print(f'User: "{prompt}"')
                    print(f'Assistant: "{response}"\n')

            results.append({
                "prompt": prompt,
                "results": [{
                    "sampling_config": sampling_config,
                    "sampling_params": sampling_params,
                    "outputs": [response],
                }]
            })
    finally:
        with open(output_file, "w") as f:
            json.dump(sampling_report, f, indent=2)

    time.sleep(1)

    # Close browser
    driver.quit()

if __name__ == '__main__':
    args = parse_args()
    main(args)
