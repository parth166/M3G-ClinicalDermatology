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

# ----------------------RETRIEVE---------------------

def retrieve(directory, input_file, images):
  input_file_path = os.path.join(directory, input_file)
  data = json.load(open(input_file_path))

  for i, encounter in enumerate(data):
    query = str(encounter["query_title_en"] + ". " + encounter["query_content_en"])
    i_paths = [os.path.join(directory, images, img) for img in encounter['image_ids']]

    payload = create_payload(model_image, system_message=guidelines.replace("{{query}}", query), query="", image_paths=i_paths)
    response = requests.post(api_base, headers=headers, json=payload)

    with open(os.path.join(directory, "retrieved.json"), "a") as f1:
      f1.write(json.dumps(response.json()) + "\n")

# -------------------- GET CANDIDATE DISEASES ------------------

def get_candidates(directory, file_name="retrieved.json"): 
  file = os.path.join(directory, file_name)
  data = [json.loads(line) for line in open(file).readlines()]

  for i, obj in enumerate(data):
    query = obj["choices"][0]['message']['content']
    payload = create_payload(model_text, system_message=create_diseases.replace("{{Text}}", query), query="", image_paths=None)
    response = requests.post(api_base, headers=headers, json=payload)

    with open(os.path.join(directory, "candidates.json"), "a") as f1:
      f1.write(json.dumps(response.json()) + "\n")

# ------------------ RANKER MODULE --------------------------
def re_ranker(directory, input_file, images):
  data = json.load(open(os.path.join(directory, input_file)))
  candidates = [json.loads(line) for line in open(os.path.join(directory, 'candidates.json')).readlines()]

  for i, encounter in enumerate(data):
    obj = json.loads(candidates[i]["choices"][0]['message']['content'])
    candidates = obj['possible_diseases']
    i_paths = [os.path.join(directory, images, img) for img in encounter['image_ids']]
    payload = create_payload(model_image, system_message=image_description_similarity.replace("{{Candidates}}", str(candidates)), query="", image_paths=i_paths, max_tokens=1400)
    response = requests.post(api_base, headers=headers, json=payload)

    with open(os.path.join(directory, "top_2_candidates.json"), "a") as f1:
      f1.write(json.dumps(response.json()) + "\n")

# -------------- GNERATE RESPONSES --------------------------

def generate_response(directory, input_file):
  data = [json.loads(line) for line in open(os.path.join(directory, 'top_2_candidates.json')).readlines()]
  test_dataset = json.load(open(os.path.join(directory, input_file)))

  for i, obj in enumerate(data):
    notes = obj['choices'][0]['message']['content']
    payload = create_payload(model_text, system_message=generate_response_for_top2.replace("{{Text}}", str(notes)), query="", image_paths=None, max_tokens=100)
    response = requests.post(api_base, headers=headers, json=payload)

    with open(os.path.join(directory, "final_preds.json"), "a") as f1:
      f1.write(json.dumps(response.json()) + "\n")

# ------------------ FINAL RESPONSE FORMATTER----------------

def create_final_response(directory, input_file):
  data = [json.loads(line) for line in open(os.path.join(directory, 'final_preds.json')).readlines()]
  test_dataset = json.load(open(os.path.join(directory, input_file)))

  arr = []
  for i, obj in enumerate(data):
    final_res = obj['choices'][0]['message']['content']
    
    response = {
      "encounter_id": test_dataset[i]["encounter_id"],
      "responses": [{"content_en": final_res, "content_zh": "", "content_es": ""}]
    }
    arr.append(response)

  with open(os.path.join(directory, "prediction.json"), "a") as f1:
    f1.write(json.dumps(arr) + "\n")

# ----------------- MAIN -----------------------

def main():
  """
    The pipeline is as follows:
    
    directory structure should be as follows

    directory_name
      |____ input.json
      |____ input_test
            |______ img1.jpg
            .

  """
  directory_name = "./final_test" # replace the directory name here that contains input file (json) and images. Also, make sure, this directory is on your current path.
  input_file_name = "input.json" # the input file name in your directory
  input_images_dir = "images_test" # the images folder in your directory

  assert os.path.exists(os.path.join(directory_name, input_file_name)), "An exact path cannot be found to the give file name, check directory structure"
  assert os.path.exists(os.path.join(directory_name, input_images_dir)), "An exact path cannot be found to the input images, check directory structure"
  
  # # step 1
  retrieve(directory_name, input_file_name, input_images_dir) # this is the retriever module

  # # step 2
  get_candidates(directory_name) # this methods create a list of possible candidates from step 1

  # step 3
  re_ranker(directory_name, input_file_name, input_images_dir) # this is the Ranker module

  # step 4 
  generate_response(directory_name, input_file_name) # this is the geration module

  # step 5
  create_final_response(directory_name, input_file_name) # final output in a clean format as expected by ClinicalNLP workshop M3G

if __name__ == '__main__':
  main()
