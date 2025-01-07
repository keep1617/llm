from datasets import load_dataset
import huggingface_hub
import pandas as pd
import json
import jsonlines
from datasets import Dataset
import os

huggingface_hub.login('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')

ds = load_dataset("adfa5456/bartender")





def create_text_column(example):
    text = f"### instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    example["text"] = text
    return example

ds = ds.map(create_text_column)

print(ds['train']['text'])