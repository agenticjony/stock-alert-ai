import os
import json
from openai import OpenAI

# Initialize OpenAI client safely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key-fallback")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_news_sentiment(news_list):
    if not news_list:
        return {"sentiment_score": 0, "reason": "No recent headlines discovered."}
        
    news_text = ""
    for article in news_list[:5]:
        news_text += f"Title: {article.get('title')}\nSummary: {article.get('text')}\n---\n"
        
    prompt = f"""
    Analyze the following news articles and rate from -10 to +10.
    Consider: Product launches, Government contracts, New customers, AI exposure, Earnings surprises, Analyst upgrades.
    
    News Articles:
    {news_text}
    
    Output ONLY in this exact string format without markdown or extra words:
    Bullish Score: <number> | Reason: <one sentence summary>
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a quantitative financial sentiment parser."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        result_text = response.choices[0].message.content.strip()
        
        if "|" in result_text:
            score_part, reason_part = result_text.split("|", 1)
            raw_score = score_part.replace("Bullish Score:", "").strip()
            sentiment_score = float(raw_score)
            reason = reason_part.replace("Reason:", "").strip()
        else:
            sentiment_score = 0
            reason = result_text
            
        return {"sentiment_score": sentiment_score, "reason": reason}
        
    except Exception as e:
        return {"sentiment_score": 0, "reason": f"AI Parsing skipped: {str(e)}"}