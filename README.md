# Open-Assistant Model Evaluation

This repository contains tools used during Open-Assistant development to measure the OA model and potential base models and is used to collect sampling reports.


## Generating Sampling Reports

### Installation
1. Make sure `python 3.10.0` is installed.
2. Create a virtual environment: `python3.10 -m venv .venv`
3. Activate the venv: `source .venv/bin/activate`
4. Installed dependencies by executing `pip install -r requirements.txt` in the root directory of this repository.

### Sampling
You can use the script `model_eval/manual/sampling_report.py` to generate continuations for a number of prompts specified in a jsonl file with sampling parameters defined in a configuration file. You find 100 random prompts from the Open-Assistant prompt database in the file `data/en_100_text.jsonl` and simple sampling configurations in the `config/` directory.

Example command to run `sampling_report.py` with `facebook/galactica-125m` (a small model good for testing):

```sh
python sampling_report.py --model-name facebook/galactica-125m --config config/default.json --prompts data/en_100_text.jsonl --report report_file.json --verbose --num-samples 2 --half
```

### CLI arguments

```
$ python sampling_report.py --help
Using pytorch version 1.13.1+cu117
usage: sampling_report.py [-h] [--device DEVICE] [--device-index DEVICE_INDEX] [--model-name MODEL_NAME] [--mode MODE] [--prompts PROMPTS] [--report REPORT] [--seed SEED] [--verbose] [-n N]
                          [--num-samples NUM_SAMPLES] [--config CONFIG] [--half] [--skip-special-tokens] [--model-type MODEL_TYPE] [--max-input-len MAX_INPUT_LEN]

options:
  -h, --help            show this help message and exit
  --device DEVICE       device to use
  --device-index DEVICE_INDEX
                        device index
  --model-name MODEL_NAME
  --mode MODE           legacy, v2
  --prompts PROMPTS     jsonl string prompts input file name
  --report REPORT       json sampling report output file name
  --seed SEED           psoudo random number generator seed
  --verbose
  -n N                  number of promtps to use (default: all)
  --num-samples NUM_SAMPLES
                        number of sampling runs per configuration
  --config CONFIG       configuration file path
  --half                use float16
  --skip-special-tokens
  --model-type MODEL_TYPE
                        CausalLM, T5Conditional
  --max-input-len MAX_INPUT_LEN
                        max token counts for input
```


Once the report file has been generated you can use the Model Output Comparer to compare the sampling results with different other outputs.

## Model Ouptput Comparer

Use the [Model Output Comparer](https://open-assistant.github.io/oasst-model-eval/) to compare sampling results of different models and standard Huggingface Transformers sampling configurations.

You can load json report files by either specifying their URLs or by clicking into the file drop-zone and selecting a file in the browsers file-selector. As the name implies you can also drop files to the drop-zone (drag & drop).

You can select some models form the [sampling_reports](https://github.com/Open-Assistant/oasst-model-eval/tree/main/sampling_reports) folder for comparison.

Here are some example URLs you can copy & paste into the input box directly below the **Model Output Comparer** title as an example:

```
https://raw.githubusercontent.com/Open-Assistant/oasst-model-eval/main/sampling_reports/pythia/2023-03-01_theblackcat102_pythia-3b-deduped-sft_sampling_default.json
https://raw.githubusercontent.com/Open-Assistant/oasst-model-eval/main/sampling_reports/chip2_7b_instruct_alpha/2023-03-02_chip2_7b_instruct_alpha_sampling_default.json
https://raw.githubusercontent.com/Open-Assistant/oasst-model-eval/main/sampling_reports/bloomz-7b1-mt/2023-03-02_bigscience_bloomz-7b1-mt_sampling_default.json
```


## Commands to deploy web model comparer to gh-pages 

To run a front-end tool to compare model outputs, do:

```sh
cd model_comparer
npm start
```

See the `model_comparer/README.md` for more information.

To deploy to github pages:

```sh
cd model_comparer
npm install
npm run deploy
```
