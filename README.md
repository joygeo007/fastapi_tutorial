# AI News Summarizer: A FastAPI & Google Gemini Tutorial

This repository contains the source code for the AI News Summarizer, a web application built with FastAPI and powered by the Google Gemini API. It's designed as a comprehensive tutorial for developers who want to learn FastAPI quickly by building a practical, real-world project.

The application fetches real-time news headlines from various categories, and when a user is interested in an article, it generates a concise summary on-demand using a powerful generative AI model.

## Features

  * **Real-time News:** Fetches the latest headlines from NewsAPI across multiple categories.
  * **On-Demand AI Summarization:** Instead of summarizing everything at once, it generates a summary for a specific article only when the user requests it, making the application fast and efficient.
  * **Modern Python Backend:** Built with FastAPI, showcasing its speed, simplicity, and features like automatic data validation and API documentation.
  * **Cloud-Powered AI:** Integrates with the Google Gemini API for high-quality, state-of-the-art text summarization.
  * **Interactive Frontend:** A simple and clean HTML and JavaScript interface to interact with the backend services.
  * **Best Practices:** Demonstrates key development practices like using virtual environments, managing API keys securely with `.env` files, and structuring a project for clarity.

## Technology Stack

  * **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
  * **AI Model:** [Google Gemini API](https://ai.google.dev/)
  * **News Source:** [NewsAPI](https://newsapi.org/)
  * **Data Validation:** [Pydantic](https://pydantic-docs.helpmanual.io/)
  * **HTTP Requests:** [Requests](https://requests.readthedocs.io/en/latest/)
  * **Environment Variables:** [python-dotenv](https://pypi.org/project/python-dotenv/)
  * **Frontend:** HTML, CSS, JavaScript

## Project Structure

A well-organized project structure is key to a maintainable application. We follow a standard, intuitive layout:

```
news-summarizer/
├── venv/                    # Python virtual environment (ignored by Git)
├── app/
│   ├── __init__.py          # Makes 'app' a Python package
│   └── main.py              # Core FastAPI application logic
├── static/
│   └── index.html           # The HTML/CSS/JS frontend
├── .env                     # Stores secret API keys (you will create this)
├── .gitignore               # Tells Git which files to ignore
└── requirements.txt         # Lists all Python project dependencies
```

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1\. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/joygeo007/fastapi_tutorial.git
cd news-summarizer
```

### 2\. Set Up a Python Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)`.

### 3\. Install Dependencies

Install all the required Python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4\. Obtain API Keys

This project requires two free API keys:

  * **NewsAPI Key:**

    1.  Go to [newsapi.org](https://newsapi.org/) and register for a free developer account.
    2.  Once registered, find and copy your API key.

  * **Google Gemini API Key:**

    1.  Go to [Google AI Studio](https://aistudio.google.com/).
    2.  Sign in with your Google account and click on **"Get API key"**.
    3.  Create and copy your new API key.

### 5\. Configure Environment Variables

API keys are secrets and should never be hardcoded in your source code. We use a `.env` file to manage them securely.

1.  In the root of the project directory, create a new file named `.env`.

2.  Add your API keys to this file as shown below, replacing the placeholders with your actual keys:

    ```.env
    NEWS_API_KEY=your_actual_newsapi_key_here
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

The `.gitignore` file is already configured to ignore the `.env` file, ensuring you don't accidentally commit your secrets to a public repository.

## Running the Application

With everything set up, you're ready to run the FastAPI server\!

1.  Make sure your virtual environment is activated.

2.  Run the main application file from the project's root directory:

    ```bash
    python app/main.py
    ```

3.  Uvicorn, the ASGI server, will start. You will see output like this in your terminal:

    ```
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```

4.  Open your web browser and navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)**. You should see the AI News Summarizer interface.

## FastAPI Tutorial: A Code Deep Dive

This section breaks down the code to explain the core FastAPI concepts it demonstrates.

### `app/main.py` - The FastAPI Backend

This file is the heart of our application. Let's explore its key components.

#### 1\. Pydantic Models: Defining Your Data's "Shape"

FastAPI uses Pydantic models to define the structure and data types of your API's inputs and outputs. This gives you powerful data validation, serialization, and documentation for free.

```python
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
```

  * `Article`: Defines the structure of a news article object that we get from NewsAPI.
  * `SummarizeRequest`: Defines the expected structure of the `POST` request body when the frontend asks for a summary. FastAPI will automatically validate that incoming requests have a `content` field that is a string.
  * `SummaryResponse`: Defines the structure of the JSON response sent back after summarisation.

#### 2\. API Endpoints (Path Operations)

Endpoints are the different URLs of your API. In FastAPI, you create them using "path operation decorators" like `@app.get()` and `@app.post()`.

**Serving the Frontend (`@app.get("/")`)**

```python
from fastapi.responses import FileResponse

@app.get("/")
async def serve_homepage():
    return FileResponse("static/index.html")
```

This is the simplest endpoint. When a user accesses the root URL (`/`), it serves the `index.html` file as the response.

**Fetching News Articles (`@app.get("/fetch_news")`)**

```python
@app.get("/fetch_news", response_model=List[Article])
async def fetch_news(category: str = Query("technology", ...)):
    # ... logic to call NewsAPI ...
    return articles
```

  * `@app.get("/fetch_news")`: Creates a `GET` endpoint at the `/fetch_news` URL.
  * `response_model=List[Article]`: This is a powerful FastAPI feature. It declares that the response of this function will be a JSON array of objects, where each object conforms to the structure of our `Article` Pydantic model. FastAPI uses this to validate outgoing data and to generate the API documentation.
  * The function calls NewsAPI, processes the results, and returns a list of `Article` objects.

**Summarizing a Single Article (`@app.post("/summarize_article")`)**

```python
@app.post("/summarize_article", response_model=SummaryResponse)
async def summarize_article(request: SummarizeRequest):
    # ... logic to call Gemini API ...
    return SummaryResponse(summary=summary)
```

  * `@app.post(...)`: We use `POST` because the client is sending a block of data (the article content) to the server in the request body.
  * `request: SummarizeRequest`: This is where the magic happens. FastAPI automatically reads the body of the `POST` request, parses it as JSON, and validates it against the `SummarizeRequest` model. If the JSON is malformed or missing the `content` field, FastAPI automatically returns a helpful error response.
  * The function takes the content, sends it to the Gemini API, and returns the result wrapped in our `SummaryResponse` model.

### `static/index.html` - The Frontend

The frontend is a single HTML file with embedded CSS and JavaScript. The JavaScript uses the `fetch` API to communicate with our FastAPI backend.

  * **`fetchArticles()` function:** Makes a `GET` request to our `/fetch_news` endpoint. It then dynamically builds the HTML to display the list of headlines and "Read More" buttons.
  * **`expandSummary()` function:** Triggered when a "Read More" button is clicked. It makes a `POST` request to our `/summarize_article` endpoint, sending the specific article's content in the request body. When it receives the summary, it injects it into the page.

## Explore the Interactive API Docs

FastAPI automatically generates interactive API documentation for your project based on your Pydantic models and path operations. This is one of its most beloved features.

  * Navigate to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

You will see a Swagger UI interface where you can view, test, and interact with each of your API endpoints directly from your browser. This is incredibly useful for debugging and for understanding how your API works without needing a frontend.

## Next Steps & Potential Enhancements

This project provides a solid foundation. Here are some ideas for how you could extend it:

  * **Caching:** Implement caching for NewsAPI responses to reduce redundant calls and speed up the application.
  * **Database Integration:** Store fetched articles and their summaries in a database like SQLite or PostgreSQL to create a history of summarised content.
  * **Improved UI:** Use a frontend framework like Vue.js or React to build a more sophisticated and dynamic user interface.
  * **Advanced Error Handling:** Add more specific error messages on the frontend to improve the user experience when an API call fails.
  * **Deployment:** Containerise the application using Docker and deploy it to a cloud service like Google Cloud Run or AWS Elastic Beanstalk.
