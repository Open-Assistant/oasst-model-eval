# Model-output comparer

We have now a little python script that generates completions for random prompts from our dataset
with different sampling parameters. The result is stored as a json report. This tools allows you
to manually compare outputs of different base-models and the fine-tuning result models. This is
a comparison UI that allows to inspect 10+ report files.

The json reports have the following properties:

- Each file contains information about the models
- Each file contains a list of prompts (which are always identical between the different models,
  same prompts in the same order), for each prompt there are multiple sampling configurations
  (which are also identical across models per prompt, but NOT across prompts)
    - for each sampling configuration we have the same number of outputs.


Example report files:

https://github.com/LAION-AI/Open-Assistant/tree/main/model/model_eval/manual/sampling_reports

Building
========

```sh
npm install
npm start
```
