import os
import sys
import subprocess

# Force the user-installed packages into the path
user_base = subprocess.check_output(['python3', '-m', 'site', '--user-site']).decode('utf-8').strip()
sys.path.append(user_base)

import json
import random
import re

try:
    import google.generativeai as genai
except ImportError:
    # Final fallback attempt
    print(f"Module still not found. Searched in: {sys.path}")
    sys.exit(1)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

topics = ["Potomac River levels", "Cacapon River padding", "Sleepy Creek trails", "Appalachian ridge hiking"]

def generate():
    topic = random.choice(topics)
    prompt = f"Create a tactical outdoor report about {topic} for 'Trails to Eden'. Return ONLY a JSON object: {{\"id\":\"{random.randint(100,999)}\",\"title\":\"Title\",\"excerpt\":\"Hook\",\"region\":\"WV/MD\",\"img\":\"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600\",\"content\":\"<h2>Title</h2><p>Body HTML...</p>\"}}"
    
    try:
        response = model.generate_content(prompt)
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            data = json_match.group()
            with open("data.js", "w", encoding="utf-8") as f:
                f.write(f"const localArticles = [{data}];")
            print("Successfully updated data.js")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate()
