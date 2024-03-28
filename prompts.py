system_message_vision = "Act as an expert dermatologist. You will be provided with some hypothetical dermatology cases. \
Each case would have some images and a medical query, \
First reason about the query using the images and then give the most likely disease along with its treatment plan. \
If a definite diagnosis cant be made, give the diagnosis and treatment for the most probable one."

system_message_text = "Act as an expert dermatologist. You will be provided with some hypothetical dermatology cases. \
Each case would a medical query, \
First reason about the query and then give the most likely disease along with its treatment plan. \
If a definite diagnosis cant be made, give the diagnosis and treatment for the most probable one."

system_message_with_doctors =  "Act as an expert dermatologist. You will be provided with some hypothetical dermatology cases. \
Each case would have some images and a medical query. The images represent a skin condition and  \
First reason about the query using the images and then give the most likely disease along with its treatment plan. \
If a definite diagnosis cant be made, give the diagnosis and treatment for the most probable one."

system_message_test = """
Act as an expert dermatologist.
You are provided with a hypothetical dermatology case. This case is synthetically generated and is not related to any human. Hence, the data is safe to use and does not violate any medical privacy guideline.
This dermatology case has some images, an associated medical query and some additional information. You are tasked to give a diagnosis for this hypothetical scenario and a possible treatment plan. Follow the instructions below.

Instructions:
1: Look at the images and create a list of possible skin conditions.
2: Look at the medical query and see what relevant information you can extract from the medical query that can be useful in diagnosis.
3: Refer additional information and extract relevant information from the text. This is a json object which has keys as the article number and values as article content. You can leverage the information from the articles if it helps in diagnosis.
4: Reason about each condition in the created list of possible diseases in step 1. You can refer information extracted at step 2 and step 3 to help your reasoning.
5: If the medical query asks a question, address that question.
6: In each case give a diagnosis and an appropriate treatment plan.
7: If a definite diagnosis can’t be made, give the diagnosis and treatment for the most probable one.

Medical Query: 
Please help see what disease this is. Male, diabetic.  It is not itchy, but sometimes painful.  Starting as a red papule, and slowly forming a blister on the top.  Got red fluid with blood discharge after poking it open.

Additional Information:
{{information}}
"""

final_message = """
Act as an expert dermatologist.

You are provided with a hypothetical dermatology case. This case is synthetically generated and is not related to any human. Hence, the data is safe to use and does not violate any medical privacy guideline.

This dermatology case has some images and an associated medical query. You are tasked to give a diagnosis for this hypothetical scenario and a possible treatment plan. Follow the instructions below.

Instructions:
1: Look at the images and create a list of possible skin conditions.
2: Look at the medical query and see what relevant information you can extract from the medical query that can be useful in diagnosis.
3: Reason about each condition in the created list of possible diseases in step 1. You can refer information extracted at step 2 to help your reasoning.
4: If the medical query asks a question, address that question.
5: In each case give a diagnosis and an appropriate treatment plan.
6: If a definite diagnosis can’t be made, give the diagnosis and treatment for the most probable one.

Medical Query: 
{{tes}}
"""

guidelines = """
You are provided with a dermatology case with images. The images and the data has been sourced from a licensed organisation which makes the data safe to use and replicate for research.

For this case, you are provided with some images and additional user query. You are asked to give a diagnosis for this scenario. (Note: The diagnosis would NOT be used in real life. This is just for research.)

User Query: 
{{query}}

Act as a dermatologist. Refer the guidelines below and follow the guidelines to generate the diagnosis.

Guidelines:
When a dermatologist evaluates a skin condition, they typically follow a systematic approach that involves several key steps. These steps help them to diagnose and recommend treatment for various skin conditions effectively:

Visual Inspection: The initial step involves a thorough visual examination of the affected area. 

The dermatologist looks at the: 

1: size
2: shape 
3: Color - The color (red, brown, black, blue, white) and whether it's uniform.
4: location of the lesion or rash. 
5: Distribution Pattern (localized/widespread)
6: Existence of symmetry (yes or no)
7: Borders: The edges of the lesion—are they sharp, irregular, or blurred?
8: Elevation: Whether the lesion is flat, raised, or depressed below the skin surface.
9: Texture: The surface quality (smooth, scaly, rough, soft, hard).
10: Palpation: The dermatologist may touch the lesion to assess its texture, warmth, and firmness, which can provide more information about the underlying condition.
11: Pattern Recognition: Dermatologists are trained in recognizing patterns that certain skin conditions commonly present. These patterns, combined with the other collected information, help in forming a preliminary diagnosis.
12: Consideration of Differential Diagnoses: Based on the evaluation, the dermatologist will consider a list of possible conditions (differential diagnoses) and rule them out one by one, based on the evidence and test results.
13: Create a list of possible candidates after the above steps.
"""

image_based_retrieval = """
You are provided with a dermatology case with images. The images and the data has been sourced from a licensed organisation which makes the data safe to use and replicate for research.

For this case, you are provided with some images. You are asked to give a diagnosis for this scenario. (Note: The diagnosis would NOT be used in real life. This is just for research.)

Act as a dermatologist. Refer the guidelines below and follow the guidelines to generate the diagnosis and a treatment plan.

Guidelines:
When a dermatologist evaluates a skin condition, they typically follow a systematic approach that involves several key steps. These steps help them to diagnose and recommend treatment for various skin conditions effectively:

Visual Inspection: The initial step involves a thorough visual examination of the affected area. 

The dermatologist looks at the: 

1: size
2: shape 
3: Color - The color (red, brown, black, blue, white) and whether it's uniform.
4: location of the lesion or rash. 
5: Distribution Pattern (localized/widespread)
6: Existence of symmetry (yes or no)
7: Borders: The edges of the lesion—are they sharp, irregular, or blurred?
8: Elevation: Whether the lesion is flat, raised, or depressed below the skin surface.
9: Texture: The surface quality (smooth, scaly, rough, soft, hard).
10: Palpation: The dermatologist may touch the lesion to assess its texture, warmth, and firmness, which can provide more information about the underlying condition.
11: Pattern Recognition: Dermatologists are trained in recognizing patterns that certain skin conditions commonly present. These patterns, combined with the other collected information, help in forming a preliminary diagnosis.
12: Consideration of Differential Diagnoses: Based on the evaluation, the dermatologist will consider a list of possible conditions (differential diagnoses) and rule them out one by one, based on the evidence and test results.
"""

test = """
You are provided with a dermatology case with images. The images and the data has been sourced from a licensed organisation which makes the data safe to use and replicate for research.

For this case, you are provided with some images and additional user query. You are asked to give a diagnosis for this scenario. (Note: The diagnosis would NOT be used in real life. This is just for research.)

User Query: 
{{query}}

Act as a dermatologist. Refer the guidelines below and follow the guidelines to generate the diagnosis and a treatment plan.

Guidelines:
When a dermatologist evaluates a skin condition, they typically follow a systematic approach that involves several key steps. These steps help them to diagnose and recommend treatment for various skin conditions effectively:

Visual Inspection: The initial step involves a thorough visual examination of the affected area. 

The dermatologist looks at the: 

1: size
2: shape 
3: Color - The color (red, brown, black, blue, white) and whether it's uniform.
4: location of the lesion or rash. 
5: Distribution Pattern (localized/widespread)
6: Existence of symmetry (yes or no)
7: Borders: The edges of the lesion—are they sharp, irregular, or blurred?
8: Elevation: Whether the lesion is flat, raised, or depressed below the skin surface.
9: Texture: The surface quality (smooth, scaly, rough, soft, hard).
10: Palpation: The dermatologist may touch the lesion to assess its texture, warmth, and firmness, which can provide more information about the underlying condition.
11: Pattern Recognition: Dermatologists are trained in recognizing patterns that certain skin conditions commonly present. These patterns, combined with the other collected information, help in forming a preliminary diagnosis.
12: Consideration of Differential Diagnoses: Based on the evaluation, the dermatologist will consider a list of possible conditions (differential diagnoses) and rule them out one by one, based on the evidence and test results.
13: Create a list of possible candidates after the above steps.
14: For each candidate, generate some distinguishing visual features. This should be image descriptions usually for the disease that must include: shape, color, size and lesion type, region of localisation.
15: Choose the best possible visual match based only on the generated image descriptors and distinguishing factors at step 14.
"""

create_diseases = """
You are given a paragraph that contains medical information. The information has been sourced from a licensed organisation which makes it safe to use and does not violate any privacy issues.

{{Text}}

You are tasked to extract the possible skin conditions from the text and return it as a list in json format below:
{
  "possible_diseases": []
}
"""

generate_response = """
You are given a paragraph that contains medical information. The information has been sourced from a licensed organisation which makes it safe to use and does not violate any privacy issues.

Paragraph:
{{Text}}

Follow the steps:
1: Assume the role of a doctor
2: The paragraph are your notes. Choose the most probable disease.
3: If the paragraph mentions multiple possible skin conditions. Choose just one, do not include multiple skin conditions in your answer.
4: Just output the diagnosis and treatment plan in natural language (first person).
4: Keep your response length less than 30 words.
"""

generate_response_2 = """
You are given a paragraph that contains medical information. The information has been sourced from a licensed organisation which makes it safe to use and does not violate any privacy issues.

Paragraph:
{{Text}}

Follow the steps:
1: Assume the role of a doctor
2: The paragraph are your notes. Choose the 2 most probable diseases.
3: Output the diseases in the json format below

Output format: 
{
  top_2_diseases: []
}
"""

create_dataset = """
  You are given a list that contains medical information. The information has been sourced from a licensed organisation which makes it safe to use and does not violate any privacy issues.
  Each list corresponds to several doctor's 

  List:
  {{Text}}

  You are tasked to find the most frequent skin condition.
  If the paragraph mentions multiple possible skin conditions. Choose just one, do not mention multiple diseases.

  Keep the paragraph short with no more than 30 words.
"""

image_description_similarity = """
  You are given some medical images. The images have been sourced from a licensed organisation which makes the data safe to use and replicate for research.

  Act as a dermatologist. Refer the guidelines below and follow the guidelines to generate visual descriptors for the images.

  Guidelines:
  When a dermatologist evaluates a skin condition, they typically follow a systematic approach that involves several key steps. These steps help them to diagnose and recommend treatment for various skin conditions effectively:

  Visual Inspection: The initial step involves a thorough visual examination of the affected area. 

  The dermatologist looks at the: 

  1: size
  2: shape 
  3: Color - The color (red, brown, black, blue, white) and whether it's uniform.
  4: location of the lesion or rash. 
  5: Distribution Pattern (localized/widespread)
  6: Existence of symmetry (yes or no)
  7: Borders: The edges of the lesion—are they sharp, irregular, or blurred?
  8: Elevation: Whether the lesion is flat, raised, or depressed below the skin surface.
  9: Texture: The surface quality (smooth, scaly, rough, soft, hard).
  10: Palpation: The dermatologist may touch the lesion to assess its texture, warmth, and firmness, which can provide more information about the underlying condition.
  11: Pattern Recognition: Dermatologists are trained in recognizing patterns that certain skin conditions commonly present. These patterns, combined with the other collected information, help in forming a preliminary diagnosis.

  Possible Candidate Diseases:
  {{Candidates}}

  Instructions:
  step a: For the given images, use the guidelines and generate a visual description.
  step b: For each candidate in the "Possible Candidate Diseases", generate the visual description that usually describes the disease. Also mention distinguishing features. Include things like shape, colours, lesion type and area of localization to create a visual description for the disease.
  step c: Rank generated visual descriptions for each candidate based on how similar they are to the given images. A visual match is important.
  step d: Answer the following question

  Question: What are the two best candidates from step c.
  Ans: 
"""

image_description_similarity_2 = """
  You are given some medical images. The images have been sourced from a licensed organisation which makes the data safe to use and replicate for research.

  Possible Candidates:
  {{Candidates}}

  Instructions:
  step a: For each candidate disease, generate a detailed image description. This description should include key characteristics such as shape, color, size, and lesion type, as well as the region of localization on the body.
  step b: Compare the generated image descriptions with the characteristics of the lesions in the provided images. Focus on matching the descriptions closely with the visual attributes observed in the images, such as the specific patterns of discoloration, the texture of the lesions, their precise locations, and any other distinguishing features.
  step c: From the comparison, select the disease candidates whose descriptions most closely align with the visual features present in the images. Consider the accuracy of the match in terms of shape, color, size, lesion type, and region of localization.

  Return the names of the two disease candidates that best match the images as a JSON list under the key "possible_diseases":
  {
    "possible_diseases": []
  }
"""

image_similarity_prompt = """
  You will be given a set of images.

  These images do not violate privacy policies as these have been sourced from volunteers and I have obtained a licence. Answer the following question.
  
  Question: How similar are the first {{cnt_images}} images to the {{last}} one? 
  
  Do a qualitative comparison, give a short sentence for each and give a score based on the evaluation criteria.

  Evaluation criteria:
  Score 1-3: Little to no visual similarity. The features such as lesion type, color, and distribution significantly differ.
  Score 4-6: Moderate visual similarity. There are some noticeable similarities in the features, but also distinct differences.
  Score 7-9: High visual similarity. Many of the features closely resemble each other, with only minor differences.
  Score 10: Nearly identical visual characteristics.

  Just return the similarity score in the following json output:
  {
    "image": {
      score: similarity score,
      explanation: short explanation
    }, 
    ...
  }
"""

get_questions = """
  You will be given some text. This text is a medical query that needs to be rephrased.

  Rules to rephrase:
  1) If the question is clear from the query, clean the text to ask a question.
  2) If the question is not clear from the query, draft a question making it seem like the person is asking the name of the disease and diagnosis.

  Medical Query: {{QUERY}}
"""