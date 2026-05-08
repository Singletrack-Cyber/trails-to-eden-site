import os
from google import genai
from datetime import datetime
import random

# 1. Setup Gemini Client (using environment variable)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

topics = [
    "Seasonal Conditions & Trail Reports: Tracking current weather patterns, Potomac and Cacapon River water levels, and seasonal trail maintenance updates for local gravel and mountain bike routes",
    "Regional Events & Gear Spotlight: Highlighting upcoming adventure races, community group rides, or specific equipment best suited for the rocky terrain of the Appalachian ridges",
    "Survival & Bushcraft Proficiency: Focusing on essential wilderness skills such as local forage identification, emergency shelter construction, and water filtration techniques specific to the Mid-Atlantic climate",
    "Location-Specific Exploration: Identifying unique landmarks within the DMV, from the rugged trails of Sleepy Creek to the historic paths of the C&O Canal and Green Ridge State Forest",
    "Wilderness Stewardship & Ethics: Incorporating principles of Leave No Trace and sustainable outdoor practices to preserve the natural beauty of the Great Cacapon area for future expeditions",
]

def generate_article():
    topic = random.choice(topics)
    print(f"Generating article for: {topic}")

    prompt = (
        f"Write a high-quality blog post about {topic} for the site 'Trails to Eden'. "
        "Format the output strictly as Markdown with a YAML frontmatter section at the top. "
        "Include title, date, and 3 relevant tags."
    )

    # 2. Call Gemini 3 Flash
    response = client.models.generate_content(
        model="gemini-3-flash",
        contents=prompt
    )

    content = response.text
    
    # 3. Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"content/posts/gemini-article-{timestamp}.md"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        f.write(content)

if __name__ == "__main__":
    generate_article()
