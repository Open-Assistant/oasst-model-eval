import json
import argparse
import datetime

import tqdm
import openai


def parse_args():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Enter message into URL')
    parser.add_argument('--api_key', type=str, default=None, help='URL to open')
    parser.add_argument('--base_url', type=str, default="https://openrouter.ai/api/v1", help="URL of OpenAI compatible inference end point")
    parser.add_argument('--model', type=str, default="openai/gpt-5-chat", help="model name")
    parser.add_argument('--input_file', type=str, default="data/prompt_lottery_en_250_text.jsonl", help='Path to input file')
    parser.add_argument('--num_samples', type=int, default=1, help='Number of samples to generate')
    parser.add_argument('--verbose', type=bool, default=True, help='Print output')

    # Parse arguments
    args = parser.parse_args()
    return args

def read_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
        objs = [json.loads(line) for line in lines]
    return objs

def get_response(client: openai.Client, message, **params):
    output = client.chat.completions.create(
        messages=[
            #{"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: {knowledge_cutoff} Current date: {current_date}"},
            {"role": "system", "content": "You are a helpful assistant. You give engaging, well-structured answers to user inquiries."},
            {"role": "user", "content": message},
        ],
        **params,
    )
    
    #print(output.choices[0].message)

    return output.choices[0].message.content 


def main(args):
    # Read input file
    prompts = read_input(args.input_file)

    openai.api_key = args.api_key

    client = openai.Client(api_key=args.api_key, base_url=args.base_url)
    model_name = args.model

    args_dict = dict(**args.__dict__)
    del args_dict["api_key"]
    del args_dict["verbose"]

    results = []
    sampling_report = {
        "model_name": model_name,
        "date": datetime.datetime.now().isoformat(),
        "args": args_dict,
        "prompts": results,
    }

    sampling_config = "sample"
    sampling_params = {
        "model": model_name,
        "max_tokens": 8192,
        "temperature": 0.8,
        #"top_p": 0.5,
        "frequency_penalty": 0.0,
    }

    model_name_sanitized = model_name.replace('/', '_')
    output_file = f"{datetime.datetime.now().strftime('%Y-%m-%d')}_{model_name_sanitized}_{sampling_config}.jsonl"

    try:
        for prompt in tqdm.tqdm(prompts):
            outputs = []
            for i in range(args.num_samples):
                response = get_response(client, prompt, **sampling_params)
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
                    "outputs": outputs,
                }]
            })
    finally:
        with open(output_file, "w") as f:
            json.dump(sampling_report, f, indent=2)


if __name__ == '__main__':
    args = parse_args()
    main(args)
