import os
import json
import sys
import base64
from openai import AzureOpenAI
from PIL import Image

# Setup Azure OpenAI
# You must set these environment variables:
# export AZURE_OPENAI_KEY='your-key'
# export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'
# export AZURE_OPENAI_DEPLOYMENT='gpt-4o'

api_key = os.environ.get("AZURE_OPENAI_KEY")
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

if not all([api_key, endpoint, deployment]):
    print("Error: Azure environment variables not fully set.")
    print("Required: AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT")
    sys.exit(1)

client = AzureOpenAI(
    api_key=api_key,  
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

PROMPT = """
Analyze this school timetable image and convert it into a strictly formatted JSON object.

TARGET SCHEMA:
{
  "timetable": {
    "class": "Class Name",
    "schedule": [
      {
        "day": "Monday",
        "periods": [
          {
            "period": "1",
            "time": "8:00 - 8:40",
            "options": [
              { "subject": "Subject Name", "room": null }
            ]
          }
        ]
      }
    ]
  }
}

RULES:
1. Days: Monday, Tuesday, Wednesday, Thursday, Friday.
2. Periods: 1-10 and "Lunch Period".
3. Multiple subjects in one slot? List them all in 'options'.
4. Empty slot? Use "None" as subject.
5. Accurate start/end times.
6. Output ONLY raw JSON.
"""

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def convert_image_to_json(image_path, output_path="timetable_data.json"):
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found.")
        return

    print(f"Processing image with Azure OpenAI ({deployment})...")
    
    try:
        base64_image = encode_image(image_path)
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=2000,
        )
        
        text = response.choices[0].message.content.strip()
        
        # Robust JSON extraction
        if "{" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]
            
        data = json.loads(text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully converted! Data saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_timetable.py <path_to_image.png>")
    else:
        convert_image_to_json(sys.argv[1])
