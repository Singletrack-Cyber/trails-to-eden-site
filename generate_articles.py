import os
import google.generativeai as genai
import json
import random
import re

# 1. Setup - Using the correct library name
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

topics = ["Potomac River levels", "Cacapon River padding", "Sleepy Creek trails", "Appalachian ridge hiking"]

def generate():
    topic = random.choice(topics)
    prompt = f"Create a tactical outdoor report about {topic} for 'Trails to Eden'. Return ONLY a JSON object: {{\"id\":\"{random.randint(100,999)}\",\"title\":\"Title\",\"excerpt\":\"Hook\",\"region\":\"WV/MD\",\"img\":\"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600\",\"content\":\"<h2>Title</h2><p>Body HTML...</p>\"}}"
    
    try:
        response = model.generate_content(prompt)
        # 2. Extract the JSON from the response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        
        if json_match:
            data = json_match.group()
            # 3. Write to data.js - This is what your index.html reads
            with open("data.js", "w", encoding="utf-8") as f:
                f.write(f"const localArticles = [{data}];")
            print("Successfully updated data.js")
        else:
            print("Failed to find JSON in AI response.")
            
    except Exception as e:
        print(f"Error during AI generation: {e}")

if __name__ == "__main__":
    generate()
