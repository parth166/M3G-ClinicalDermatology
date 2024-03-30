import base64
from io import BytesIO
from PIL import Image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_payload(model, system_message="", query="", image_paths=None, temperature=1.0, max_tokens=2000):
  if image_paths:
    content = [{
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{encode_image(image)}"
                }
              } for image in image_paths]
    
  messages = [
    {
      "role": "user",
      "content": [
        {
          "type": "text", 
          "text": system_message
        },
      ]
    }
  ]

  if image_paths:
    messages[0]["content"] += content

  payload = {
    "model": model,
    "messages": messages,
    "max_tokens": max_tokens,
    "temperature": temperature
  }

  return payload