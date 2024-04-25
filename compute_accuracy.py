from openai import OpenAI
import requests
import json
import os
from prompts import *
from utils import create_payload


gpt_config = json.load(open('./gpt_config.json'))
api_key = gpt_config["api_key"]
api_base = gpt_config["api_base"]

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

model_image = gpt_config['model_image']
model_text = gpt_config['model_text']

prompt = """
    Given two diseases A and B.
    
    Rules:
    1: Skin condition A is similar to B if they have same name.
    2: Skin condition A is similar to B if B is also known by the name A.
    3: Skin condition A is similar to B if both are part of the same root skin condition. Example Herpetic Eczema and seborrheic eczema are similar since they have same root, Eczema.
    4: Skin condition A is similar to B if they are both have the same effect and share a common cause. 

    Are the two skin conditions similar? Follow the rules to decide
    A: {{A}}
    B: {{B}}

    If any of the above rules is valid, the two skin conditions are similar. 
    
    Note: Do not give any explanation, just give the score 0 or 1. I don't need explanation since I want to compute
    accuracy. Json format is highly important to me.
    
    Return your answer in (json format):
    {
        similar: ...  (0 or 1)
    }
"""

def compute_accuracy(A, B): 
    payload = create_payload(model_text, system_message=prompt.replace("{{A}}", A).replace("{{B}}", B), query="", image_paths=None, max_tokens=100)
    response = requests.post(api_base, headers=headers, json=payload)
    response = response.json()['choices'][0]['message']['content']
    return json.loads(response)['similar']

def main(dir_name, data_val, ground_truth_disease, all_candidates, rank=""):
    matched = 0
    for i, candidates in enumerate(all_candidates):
        cnt = 0
        obj = {
            "encounter": ground_truth_disease[i]['encounter_id'],
            "ground_truth_disease": ground_truth_disease[i]['disease'],
            "candidates": candidates,
            "matched_candidates": [],
            "matched_status": 0
        }
        for candidate in candidates:
            res = int(compute_accuracy(candidate, ground_truth_disease[i]['disease']))
            if res == 1:
                obj["matched_candidates"].append(candidate)
                obj["matched_status"] = 1
            cnt += res

        matched += 1 if cnt > 0 else 0
        with open(os.path.join(dir_name, "re_ranker", method_name, f'accuracy_top_{rank}.json'), "a") as f1:
            f1.write(json.dumps(obj) + "\n")
    
    print(f'Matched = {matched}, All examples = {len(data_val)}, Accuracy = {matched / len(data_val)}')

if __name__ == '__main__':
    directory_name = # add the directory name here that contains input file (json) and images. Also, make sure, this directory is on your current path.
    input_file_name = # the input file name in your directory

    ground_truth = # add json file path which is an array of json objects. each json object that represents an encounter must have a "disease" field which has the ground truth. Refer the main function for dependency of objects.

    data_val = json.load(open(os.path.join(directory_name, input_file_name))) 
    ground_truth_disease = json.load(open(os.path.join(directory_name, ground_truth)))
    
    main(directory_name, data_val, ground_truth_disease, all_candidates, rank=rank)

    accuracy_file = os.path.join(directory_name, "re_ranker", method_name, f'accuracy.json')
    data = [json.loads(line) for line in open(accuracy_file).readlines()]

    matched = 0
    valid = 0
    for i, encounter in enumerate(data_val):
        cnt = 0
        for response in encounter['responses']:
            cnt += response['contains_freq_ans']
        
        if cnt == 0:
            continue

        valid += 1
        matched += data[i]['matched_status']

    print(f'Total matched = {matched}, Total valid = {valid}, Accuracy on valid examples = {matched / valid}')




