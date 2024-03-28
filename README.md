# mediqa-m3g-clinical2024

Thist dataset includes clinical dermatology textual queries and their associated images, as well as the answers to the queries.

The languages used here are Chinese (zh), English (en), and Spanish (es).


## Data Splits
The following table is the number of instances for each split.

|Train|Valid|Test|
| -------- | ------- |------- |
| 842|56|100|

There will be a Chinese, English, and Spanish version of each. All non-English train splits are machine translated from the Chinese original. All valid/test sets are human translated.

## Data Description

Input Content

(a) json list where each instance will be represented by a json object with the following attributes:

| attribute_id | description |
| -------- | ------- |
|encounter_id|unique identification string for the case|
|image_ids|list of strings of the image_id’s|
|query_title_{LANGUAGE}|a string representing the query title|
|query_content_{LANGUAGE}|a string representing the query content|

(b) image files with unique id’s

Images are stored in the following folders respectively:
images_{train,valid,test}/

Image naming convention is as follows: IMG_{ENCOUNTER_ID}_{IMAGENUM}.*

(c) df_userinfo.csv

csv where each row will include author attributes:

|attribute_id|description|
| -------- | ------- |
|author_id|unique identification string for the author|
|validation_level|validation level of the response author obtained by uploading their professional credentials (categories are: {realid_validated, md_validated, md1_validated, md2_validated, md3_validated, md4_validated}) - md{} - indicates some medical doctor certificate uploaded, the higher the number, the higher the rank. (Note: no validation level doesn’t mean author is not a doctor)|
|rank_level|author leveling system based on past useful response ratings (level_{0-8}, higher the better)|

(d) Reference data will additionally have the field:

|attribute_id|description|
| -------- | ------- |
|responses|a list of json objects with the following keys ( author_id, content_{LANGUAGE} , completeness, contains_freq_ans)|

completeness: given a score {0.0, 0.5, 1.0}, depending on if the original queries’ question was fully answered. A score of 1.0 indicates that the query was completely answered, 0.5 if partially answered, 0.0 if not answered. If no explicit query is given, we assume the query asks for a disease AND treatment.

contains_freq_ans: given a score {0.0, 1.0}. 1.0 is given if the most frequent answer.


## Output Content

Output should be json list with at least the following content

|attribute_id|description|
| -------- | ------- |
|encounter_id|unique identification string for the case|

|responses|a list of json objects with the following keys ( “content_{LANGUAGE}” ) - put your answer in first object|

## Evaluation Script

The evaluation script used in codabench is scoring_multilingresp.py.
Please be sure to change paths to your local directory when testing.


## Methodology
### Overview
The primary objective of our study was to leverage the capabilities of GPT-4, particularly its vision-enhanced variant, for the task of clinical dermatology diagnosis. Our approach combined the analytical power of GPT-4 with visual and textual data to generate differential diagnoses for various dermatological conditions.

### Dataset
Our dataset comprised two primary components: clinical dermatology images and corresponding medical queries. Each datapoint in the dataset represented a unique case, including one or more images indicative of dermatological conditions, alongside a medical query detailing the patient's symptoms and any relevant medical history.

### Procedure
**Initial Analysis with GPT-4-vision:**
For each case within our dataset, we engaged GPT-4-vision, utilizing custom prompts that combined the provided images and medical queries. This initial step aimed to leverage GPT-4's understanding of both textual and visual inputs to comprehend the context of each dermatological case.

**Differential Diagnosis Generation:**
Employing chain-of-thought reasoning strategies, we prompted GPT-4 to articulate multiple potential diagnoses for each case. This approach allowed for a broad consideration of possible conditions, acknowledging the complexity and variability inherent in dermatological diagnosis.
Distinguishing Image Descriptors:

For each candidate diagnosis, we further requested GPT-4V to generate detailed image descriptors that could serve as distinguishing features for the diseases in question. This step aimed to refine our understanding of each potential condition by identifying visual markers critical for differential diagnosis.

**Comparison and Candidate Selection:**
With the generated disease descriptions in hand, we then conducted a comparative analysis against the actual images from our dataset. This process involved matching the GPT-4V-generated image descriptors with visible features in the clinical images to identify the top two most plausible candidates for each case.

**Final Diagnosis Prediction:**
As the culmination of our methodology, we provided GPT-4 with the contextual findings from the previous step, prompting it to select the most likely disease from the top candidates. This final prediction represented GPT-4's integrated analysis of both the visual and textual data, alongside the reasoning developed throughout the process.

### Conclusion
This methodology represents a novel application of AI in the field of dermatology, harnessing the synergy between advanced language models and clinical imagery. Through iterative reasoning and detailed visual-textual analysis, our approach seeks to enhance diagnostic accuracy and efficiency in dermatological practice.
