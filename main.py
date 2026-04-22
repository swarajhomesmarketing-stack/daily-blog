import os
import feedparser
import google.generativeai as genai
from datetime import datetime

# --- CONFIG ---
GEMINI_API_KEY = os.getenv("AIzaSyBrrTosqgdXSbG-y1hL6mQ0flxYfshJfbg")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_topics():
    rss_url = "https://news.google.com/rss/search?q=Maharashtra+Real+Estate+MahaRERA+when:1d&hl=en-IN&gl=IN"
    feed = feedparser.parse(rss_url)
    return [entry.title for entry in feed.entries[:4]]

def generate_blog(topic, platform):
    prompt = f"Write an 800-word humanized, professional blog for {platform} about: {topic}. Focus on Maharashtra, India. Use local real estate terms."
    try:
        return model.generate_content(prompt).text
    except:
        return "AI Generation failed for this topic."

def main():
    topics = get_topics()
    platforms = ["WordPress", "Medium", "Blogger", "Substack"]
    
    # Create the filename with today's date
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"blogs-{date_str}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"MAHARASHTRA REAL ESTATE DAILY BLOGS - {date_str}\n")
        f.write("="*50 + "\n\n")
        
        for i in range(len(topics)):
            print(f"Writing blog {i+1}...")
            content = generate_blog(topics[i], platforms[i])
            img_url = f"https://image.pollinations.ai/prompt/luxury_real_estate_maharashtra_{topics[i].replace(' ', '_')}"
            
            f.write(f"SOURCE TOPIC: {topics[i]}\n")
            f.write(f"TARGET PLATFORM: {platforms[i]}\n")
            f.write(f"SUGGESTED IMAGE: {img_url}\n\n")
            f.write(content)
            f.write("\n\n" + "-"*30 + "\n\n")

    print(f"Successfully saved to {filename}")

if __name__ == "__main__":
    main()