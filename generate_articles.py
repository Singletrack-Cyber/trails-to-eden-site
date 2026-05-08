import os
import sys

# 1. Force a diagnostic print so we can see it in the logs
print("--- STARTING GENERATOR ---")
print(f"Python Version: {sys.version}")

try:
    import google.generativeai as genai
    import json
    import random
    import re
    print("--- LIBRARIES IMPORTED SUCCESSFULLY ---")
except ImportError as e:
    print(f"--- IMPORT ERROR: {e} ---")
    sys.exit(1)

# Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

topics = ["Potomac River levels", "Cacapon River padding", "Sleepy Creek trails", "Appalachian ridge hiking"]

def generate():
    topic = random.choice(topics)
    print(f"Targeting topic: {topic}")
    
    prompt = f"Create a tactical outdoor report about {topic} for 'Trails to Eden'. Return ONLY a JSON object: {{\"id\":\"{random.randint(100,999)}\",\"title\":\"Title\",\"excerpt\":\"Hook\",\"region\":\"WV/MD\",\"img\":\"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600\",\"content\":\"<h2>Title</h2><p>Body HTML...</p>\"}}"
    
    try:
        response = model.generate_content(prompt)
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        
        if json_match:
            data = json_match.group()
            # Write to data.js
            with open("data.js", "w", encoding="utf-8") as f:
                f.write(f"const localArticles = [{data}];")
            print("--- SUCCESS: data.js updated ---")
        else:
            print("--- ERROR: No JSON found in Gemini response ---")
            print(f"Raw Response: {response.text}")
            
    except Exception as e:
        print(f"--- ERROR DURING GENERATION: {e} ---")
        sys.exit(1)

if __name__ == "__main__":
    generate()
