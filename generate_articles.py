import os
import google.generativeai as genai
import json
import random
import re

# 1. Setup Gemini (Note: Using the standard library for reliability in Actions)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

topics = [
    "Seasonal Conditions & Trail Reports for the Potomac and Cacapon River",
    "Regional Events & Gear Spotlight for Appalachian ridge terrain",
    "Survival & Bushcraft Proficiency in the Mid-Atlantic climate",
    "Exploring the trails of Sleepy Creek and Green Ridge State Forest",
    "Wilderness Stewardship & Ethics in the Great Cacapon area"
]

def generate_article_obj():
    topic = random.choice(topics)
    print(f"Generating article for: {topic}")

    # We ask Gemini to return raw JSON that matches your index.html structure
    prompt = f"""
    Write a tactical outdoor report about {topic} for the site 'Trails to Eden'.
    Return the response ONLY as a JSON object with this exact structure:
    {{
        "id": "auto-{random.randint(100, 999)}",
        "title": "A Punchy Title",
        "excerpt": "A one-sentence hook.",
        "region": "West Virginia",
        "img": "Provide a high-quality Unsplash URL related to {topic}",
        "content": "<h2>Title</h2><p>Article body using HTML tags...</p>"
    }}
    """
    
    response = model.generate_content(prompt)
    # Extract JSON from potential markdown blocks
    json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    return None

def update_index():
    new_article = generate_article_obj()
    if not new_article:
        print("Failed to generate article object.")
        return

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # The "Search and Replace" Logic
    start_tag = "// AI_GENERATED_START"
    end_tag = "// AI_GENERATED_END"

    try:
        # Split the file to isolate the array
        parts = html.split(start_tag)
        top_half = parts[0]
        bottom_half = parts[1].split(end_tag)[1]

        # We take the new article and put it at the top of the array
        # This keeps the formatting clean for your JavaScript
        new_entry = json.dumps(new_article, indent=8)
        
        # We find the existing array content to append the new one to the front
        # For simplicity, we create a fresh array declaration starting with the new article
        updated_array = f"const localArticles = [\n{new_entry},"
        
        # Assemble the full file
        # Note: This will append the new article to whatever was previously between the tags
        inner_content = parts[1].split(end_tag)[0]
        # We strip the variable declaration from the existing content to avoid duplicates
        existing_items = inner_content.replace("const localArticles = [", "").strip()
        
        final_html = f"{top_half}{start_tag}\n{updated_array}\n{existing_items}\n    {end_tag}{bottom_half}"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(final_html)
        print("Successfully updated index.html")

    except Exception as e:
        print(f"Error: {e}. Make sure the comment tags are present in index.html.")

if __name__ == "__main__":
    update_index()
