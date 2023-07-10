# Benchmark (wip)

An experimental benchmark method employed using [faireval](https://github.com/i-Eval/FairEval) and [sampling reports](https://github.com/Open-Assistant/oasst-model-eval/tree/main/sampling_reports) to rank the performance of each model trained under the Open-Assistant initiative. The objective of this study is to automate the selection of human preferences through an automated method before finalizing which model to release.

Please note that this result is based on the lottery of 250 questions from Open Assistant, which consists of a single round of English conversation.

| Rank | Model | Elo Rating |
| --- | --- | --- |
| 1 | 🥇 [gpt-4-0314:sample] | 1240 |
| 2 | 🥈 [claude-v1.3:sample] | 1069 |
| 3 | 🥉 [vicuna-v1.0:sample] | 1053 |
| 4 |  [OpenAssistant/oasst-rlhf-2-llama-30b-7k-steps:nucleus9] | 1048 |
| 5 |  [OpenAssistant/llama-30b-super-pretrain:nucleus9] | 1031 |
| 6 |  [OpenAssistant/oasst-rlhf-1-llama-30b-3k-steps:nucleus9] | 1019 |
| 7 |  [OpenAssistant/llama-13B-all-language-32k:nucleus9] | 1000 |
| 8 |  [theblackcat102/open-llama-chat-5k:nucleus9] | 976 |
| 9 |  [OpenAssistant/oasst-rlhf-3-llama-30b-5k-steps:nucleus9] | 970 |
| 10 |  [OpenAssistant/pythia-12b-sft-v8-7k-steps:nucleus9] | 965 |
| 11 |  [theblackcat102/open-llama-chat-4k:nucleus9] | 954 |
| 12 |  [dvruette/llama-13b-pretrained-dropout:nucleus9] | 910 |
| 13 |  [VMware/open-llama-13b-open-instruct:nucleus9] | 906 |
| 14 |  [theblackcat102/starcoder-oasst-3.5k:nucleus9] | 858 |

How are they compared to human preference?

An online poll conducted on Twitter, available at [link](https://twitter.com/neurosp1ke/status/1654469704788918278?s=46), reveals that the majority of participants exhibit a preference for the 7k model as opposed to the 3k and 5k models which is the same as the poll suggest. However, it is noteworthy that the preference between the 3k and 5k models appears to conflict with the outcomes of the poll.

| Rank | Model | Elo Rating | Tweet Votes |
| --- | --- | --- | --- |
| 4 |  [OpenAssistant/oasst-rlhf-2-llama-30b-7k-steps:nucleus9] | 1048 |  35.4% |
| 6 |  [OpenAssistant/oasst-rlhf-1-llama-30b-3k-steps:nucleus9] | 1019 | 17.1%  |
| 9 |  [OpenAssistant/oasst-rlhf-3-llama-30b-5k-steps:nucleus9] | 970 | 19.4%  |
| - | [OpenAssistant/oasst-rlhf-1-llama-30b-8k-steps:nucleus9] | -  | 28% |

## Setup

Install the needed packages

```bash
pip install -r requirements.txt
```

You will also need an API key from openai to access gpt-4-0613

```
export OPENAI_API_KEY="your key"
```

Run sampling results:

```bash
python eval_gpt_review.py \
    -a <sampling file #1> <sampling file #2> \
    -s <sampling config for file #1> <sampling config for file #2> \
    -m <gpt-4-0613 or gpt-3.5-turbo-0613> \
    -o <unique comparison filename>.jsonl 
```

After finishing all your comparisons, run the analysis script

```bash
python elo_analysis.py
```

## Cost

Running the full 250 lottery prompts will cost around 24-28 USD per evaluation pair.