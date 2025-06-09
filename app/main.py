import os
import json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import google.generativeai as genai

load_dotenv()

app = FastAPI(
    title="News Summariser API",
    description="An API for summarising news articles using Gemini.",
    version="1.0.0"
)


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise RuntimeError("NEWS_API_KEY not found in the .env file.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in the .env file.")


NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL_NAME = "gemini-2.0-flash-lite"

@app.get("/")
async def serve_homepage():
    """Serve the homepage."""
    return FileResponse("static/index.html")


from pydantic import BaseModel
from typing import List, Optional

class Article(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    source_name: Optional[str] = None

class SummarizeRequest(BaseModel):
    content: str

class SummaryResponse(BaseModel):
    summary: str


@app.get("/fetch_news",response_model=List[Article])
async def fetch_and_summarise_news(
    category: str = Query("technology", description="Category of news to fetch. Default is 'technology'.")
):
    """Fetches a list of news articles from NewsAPI for a given category.Does NOT perform summarization."""
    news_params = {
        "category": category,
        "language": "en",
        "apiKey": NEWS_API_KEY,
        "pageSize": 5
    }
    try:
        news_response = requests.get(NEWS_API_URL, params=news_params)
        news_response.raise_for_status()
        news_data = news_response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"NewsAPI request failed: {str(e)}")
    

    if not news_data.get("articles"):
        raise []
    

    articles_to_summarize_data = news_data["articles"][:5]
    
    # Map the response to our Pydantic Article model
    articles = [Article(
        title=article.get('title', 'No Title Available'),
        url=article.get('url', '#'),
        description=article.get('description', 'No description available.'),
        source_name=article.get('source', {}).get('name', 'Unknown Source')
    ) for article in news_data["articles"]]

    return articles


@app.post("/summarize_article", response_model=SummaryResponse)
async def summarize_article(request: SummarizeRequest):
    """
    Receives content for a single article and returns a mid-sized summary using the LLM.
    """
    if not request.content or not request.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty.")

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        
        # A more specific prompt for a single article
        prompt = f"Based on the following news article content, provide a clear and concise summary of about 3-4 sentences. Focus on the key takeaway:\n\n---\n\n{request.content}\n\n---\n\nSummary:"
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
    except Exception as e:
        print(f"DEBUG: Gemini API request failed. Error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Gemini API request failed: {str(e)}")

    if not summary:
        summary = "The AI model could not generate a summary for this content."
        
    return SummaryResponse(summary=summary)


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
