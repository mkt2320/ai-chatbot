# QueryLink AI Chatbot

An AI-powered chatbot that answers user queries about content on the [Made with Nestlé](https://www.madewithnestle.ca/) website. This project includes dynamic web scraping, natural language summarization with contextual references, and a customizable GraphRAG module to enhance reasoning.


## Features

- Pop-out chatbot with custom icon, name, and avatars
- Typing indicator, scroll-to-bottom behavior, mobile responsiveness
- Real-time answers using scraped website content
- Summarized responses with reference links
- `/refresh` endpoint to dynamically update data from Nestlé’s website
- GraphRAG integration using `Neo4j` for structured context
- API-first design for easy integration and testing


## Technologies Used

- **Frontend** - React, TypeScript, Tailwind CSS, Vite                       

- **Backend** - FastAPI, Python, Uvicorn 

- **Web Scraping** - Playwright (`stealth mode + async crawling`)

- **Vector Store** - FAISS + SentenceTransformers (`all-MiniLM-L6-v2`)


- **GraphRAG** - Neo4j + Custom endpoints for node/edge creation & query 

- **Deployment** - Azure VM (Ubuntu 24.04 LTS), port 8000 exposed 


- **Others** - Axios, dotenv, OpenAI-compatible embedding abstraction  


## Local Setup Instructions

### Backend setup

    cd backend/
    python -m venv venv
    venv/Scripts/activate   
    python -m pip install --upgrade pip
    pip install -r requirements.txt

#### Environment Variables
Create a `.env` file in the `backend/` folder with the following:
```bash
### Scraping mode: set to 'true' for background/headless browser
SCRAPER_HEADLESS=false

### HuggingFace/Local embedding model name
EMBED_MODEL=all-MiniLM-L6-v2

### OpenAI key for embeddings or summarization
OPENAI_API_KEY=your-api-key-here

### Neo4j Graph Database credentials - Needed to connect and enhance the GraphRAG functionality.
NEO4J_URI=neo4j+s://your-neo4j-uri
NEO4J_USERNAME=your-username
NEO4J_PASSWORD=your-password
```
**Note**: `OPENAI_API_KEY`, `NEO4J_URL`, `NEO4J_USERNAME` and `NEO4J_PASSWORD` are required for functionality and must be added manually in your .env file. Credentials are excluded from the repository via .gitignore.

- Get your key at: https://platform.openai.com/account/api-keys

- Create a free DB at: https://neo4j.com/cloud/platform/aura-graph/

#### Initialize Embeddings (Required before using /chat)
After starting the backend server, you must initialize the content by calling the /refresh endpoint. This step scrapes the Nestlé website and generates embeddings.

#### Start backend first
    uvicorn main:app --reload

#### Then in a new terminal, run the /refresh endpoint using curl in Git Bash(if installed):
    curl -X POST http://127.0.0.1:8000/refresh

#### Else run "/refresh" endpoint on swagger UI
**Important**: `/refresh` endpoint must be executed before accessing the `/chat` endpoint, or you'll receive a message saying the data isn't ready

This will:
- Crawl Nestlé URLs
- Scrape content (using stealth Playwright)
- Generate embeddings
- Save them to scraped_data/ and embeddings/
--- 
### Frontend setup

#### Environment Configuration

Create a .env file inside the frontend/ directory with the following content:

    VITE_BACKEND_URL=http://127.0.0.1:8000

#### Install dependencies and run
    cd frontend/
    npm install
    npm run dev

Access at: http://localhost:5173


## Deployment on Azure

- Deployed to Azure VM using Ubuntu 24.04 LTS

- Backend runs via uvicorn on port 8000

- SSH and HTTP ports enabled

- Frontend is deployed using Netlify

## API Endpoints
- `/chat` - Accepts user query, returns answer + sources
- `/refresh` - Scrapes site content & rebuilds embeddings (background)
- `/graph/add-node` - Add a new node to GraphRAG
- `/graph/add-edge` - Create a relationship between nodes
- `/graph/query` - Query the graph for related facts

All APIs are Swagger-compatible. You can test with Postman or Swagger UI.

Swagger Docs available at: http://localhost:8000/docs

## GraphRAG Module
The GraphRAG (Graph-based Retrieval-Augmented Generation) module enriches chatbot responses by injecting contextual facts from a knowledge graph into the /chat endpoint output. This allows for structured reasoning, improved accuracy, and personalization.

#### How It Works
- A Neo4j AuraDB (free tier) instance is used to store product and concept relationships from the Nestlé domain (e.g., KitKat → Ingredients → Sustainability).

- During each /chat request:
    
    - If the query contains known node keywords (e.g., "kitkat", "sustainability"), related facts are fetched from the Neo4j graph using the `get_graph_facts` utility.

    - These facts are injected at the top of the bot's reply to guide the summarizer and improve answer relevance.
#### Adding Your Own Graph Data
- Add a new node - POST `/graph/add-node`

For example: 

    {
        "id": "kitkat",
        "label": "Product",
        "properties": {
            "description": "A popular Nestlé chocolate bar."
        }
    }

- Add a relationship - POST `/graph/add-edge`
For example:

        {
            "source_id": "kitkat",
            "target_id": "sustainability",
            "relation": "hasFocusOn" 
        }

- Query the node GET `/graph/query?node_id=kitkat`


## Known Limitations
- FAISS is used locally to meet budget limits. Azure Cognitive Search can be integrated by modifying vector_store.py.

- GraphRAG results are textual only (no visualization yet). The endpoints (`/graph/add-node`, `/graph/add-edge`, `/graph/query`) can be tested on swagger.

- Summarization is basic — it currently uses a lightweight model (`t5-small`) for performance. Accuracy and fluency can be improved by integrating more advanced models (e.g., `flan-t5-xl`, `OpenAI GPT-4`, or `Azure-hosted summarizers`).



## Additional Notes
- `scraper/scraped_data/`, `scraper/crawled_data/` and `embeddings/index_metadata.json` are autogenerated when you run `/refresh` endpoint and ignored via `.gitignore`.
- Bot uses **stealth scraping** to bypass anti-bot protections (Playwright in `headless mode`).
- Summarization uses default summarizer from HuggingFace pipeline or placeholder logic.
