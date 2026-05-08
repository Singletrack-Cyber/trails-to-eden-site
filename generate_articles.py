import os
import google.generativeai as genai
import json
import random
import re

# Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

topics = ["Potomac River levels", "Cacapon River padding", "Sleepy Creek trails", "Appalachian ridge hiking"]

def generate():
    topic = random.choice(topics)
    prompt = f"Create a tactical outdoor report about {topic} for 'Trails to Eden'. Return ONLY a JSON object: {{\"id\":\"{random.randint(100,999)}\",\"title\":\"Title\",\"excerpt\":\"Hook\",\"region\":\"WV/MD\",\"img\":\"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600\",\"content\":\"<h2>Title</h2><p>Body HTML...</p>\"}}"
    
    response = model.generate_content(prompt)
    json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
    
    if json_match:
        data = json_match.group()
        # This writes the data to the small helper file
        with open("data.js", "w") as f:
            f.write(f"const localArticles = [{data}];")
        print("data.js updated successfully.")

if __name__ == "__main__":
    generate()
