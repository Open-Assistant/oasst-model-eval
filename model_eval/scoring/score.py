import argparse
import os
import json
from dataset import get_dataloader
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np
import pandas as pd

def load_sampling_data(path):

    if os.path.exists(path):
        data = json.load(open(path))
    else:
        raise FileNotFoundError(f"Sampling data {path} not found")
  
    if "prompts" not in data.keys():
        raise KeyError("sampling data should contain prompts key")

    keys = set(data["prompts"][0].keys())
    required_keys = set(["prompt","results"])
    keys = keys.intersection(required_keys)
    if keys != required_keys:
        raise KeyError(f"Missing keys {required_keys - keys} ")
    
    return data
    
def batch_inference(model, dataloader):

    scores, sampling = [],[]
    for i, data in enumerate(dataloader):
        sampling.append(data.pop("sampling").cpu().detach().numpy())
        data = {k:v.squeeze() for k,v in data.items()}
        pred = model(**data).logits[:,0].cpu().detach().numpy()
        scores.append(pred)

    return np.hstack(sampling),np.hstack(scores)
        


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--data_path", type=str, help="Path of the sampling data file")
    parser.add_argument("--model_path", type=str, help="Path or url of the model file")
    parser.add_argument("--device", type=str, help="device",default="cpu")
    parser.add_argument("--save", type=bool, help="whether to save the results",default=True)


    args = parser.parse_args().__dict__
    if args.get("device")!="cpu":
      device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')
    else:
      device = torch.device('cpu')

    data = load_sampling_data(args.get("data_path"))

    reward_name = "OpenAssistant/reward-model-deberta-v3-base"
    rank_model = AutoModelForSequenceClassification.from_pretrained(reward_name)
    tokenizer = AutoTokenizer.from_pretrained(reward_name)
    rank_model.eval()
    rank_model.to(device)
  

    dataloader = get_dataloader(data, tokenizer, 512, 4, device)
    sampling, scores = batch_inference(rank_model, dataloader)
    print(sampling.shape,scores.shape)
    df = pd.DataFrame({"sampling":sampling,"score":scores})
    id2label = {v:k for k,v in dataloader.dataset.label2id.items()}
    df["sampling"] = df["sampling"].map(id2label)
    results = df.groupby("sampling")["score"].mean().to_dict()
    print("RESULTS: ", results)
    
    if args.get("save"):
        with open("results.json",'w') as file:
            json.dump(results,file,indent=4)





    


    