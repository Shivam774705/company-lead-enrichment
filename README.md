# LeadEnrich AI - Premium Company Profiling & Lead Enrichment System

A production-ready business intelligence extraction and profiling pipeline. It automatically crawls company websites, scrapes relevant content intelligently using fuzzy sitemap-and-homepage matching, extracts contacts using robust regex patterns, and generates deep B2B insights (core services, target customers, organizational pain points, and customized outreach hooks) using Groq's high-speed inference engine.

---

## Technical Stack
- **Backend**: Python 3.13 + Django + Django REST Framework (DRF), `requests`, `beautifulsoup4`, `lxml`, `rapidfuzz`.
- **Frontend**: React + Vite + Tailwind CSS + Axios + Lucide Icons.
- **AI Engine**: Groq SDK (`llama-3.3-70b-versatile`, fallback `llama-3.1-8b-instant`).
- **Persistence**: Thread-safe in-memory caching with persistent JSON SQLite fallback.
- **Google Colab**: Self-contained scraping and AI enrichment module.

---

## Folder Structure

```text
project-root/
│── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── .gitignore
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── enrichment/
│       ├── apps.py
│       ├── constants.py
│       ├── utils.py
│       ├── scraper.py
│       ├── ai_service.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── EnrichForm.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── ResultsTable.jsx
│   │   │   ├── SkeletonLoader.jsx
│   │   │   └── Toast.jsx
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
│── colab/
│   └── colab_notebook.py
│── README.md
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js v18 or higher
- Groq API Key (Get one from [console.groq.com](https://console.groq.com))

### 1. Backend Setup (Django)
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows (cmd):
   venv\Scripts\activate
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file from the template and configure your **Groq API Key**:
   ```bash
   # Create .env and paste your GROQ_API_KEY
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
   The backend API will run on `http://127.0.0.1:8000/`.

---

### 2. Frontend Setup (React + Vite + Tailwind)
1. Open a new terminal and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Build or run the development server:
   ```bash
   npm run dev
   ```
   The frontend app will run on `http://localhost:3000/`.

---

## API Documentation

### 1. Company Enrichment API
- **Endpoint**: `POST /api/enrich/`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "url": "https://reluconsultancy.in",
    "website_name": "Relu Consultancy"
  }
  ```
- **Response Structure (Strict Format)**:
  ```json
  {
    "website_name": "Relu Consultancy",
    "company_name": "Relu Consultancy Pvt Ltd",
    "address": "Mumbai, India",
    "mobile_number": "+91-XXXXXXXXXX",
    "mail": [
      "hiring@reluconsultancy.in"
    ],
    "core_service": "AI & Automation Developer solutions",
    "target_customer": "SMEs looking to integrate custom LLMs and RPA bots",
    "probable_pain_point": "Scaling manual cold outreach pipelines without ballooning payroll cost",
    "outreach_opener": "Hi Relu Consultancy team, noticed your focus on AI development. We help firms reduce data extraction times by 70%."
  }
  ```

### 2. Retrieve Enriched List API
- **Endpoint**: `GET /api/results/`
- **Response**: Array of all previously enriched company objects stored in memory.

---

## Core System Architecture & Features

### Smart Scraping Workflow
1. **Approach 1 (Sitemap)**: Attempt to parse the target website's `/sitemap.xml`.
2. **Approach 2 (Homepage Discovery)**: If sitemap is missing, fetch the homepage HTML and collect all internal anchor `<a>` links.
3. **Approach 3 (Fuzzy Match Scoring)**: Run `rapidfuzz` string similarity scoring against target pages containing: `about`, `contact`, `services`, `who-we-are`, `team`, `industries`, `solutions`. Take top 4 scoring paths to crawl.
4. **Approach 4 (Homepage Fallback)**: If blocked or links fail, fall back to parsing homepage text content only.

### Token Optimization & Extraction
- **Boilerplate Stripping**: Removes scripts, styles, nav menus, headers, footers, svg graphics, button widgets, and forms using BeautifulSoup.
- **Whitespace Normalization**: Compresses multi-spaces, newlines, and tabs.
- **Length Caps**: Merges crawled text and truncates to ~8500 characters, remaining extremely token-efficient.
- **Regex Extraction**: Pre-extracts emails and phone numbers *before* sending to LLM, reducing context load and providing correct keys to the model.

### Anti-Hallucination Prompts
System prompts strictly instruct Groq model `llama-3.3-70b-versatile` to only extract facts from text context or the regex-provided arrays. If a key is missing, it is forced to return `""` or `[]` for arrays, avoiding hallucinations.

---

## Google Colab Notebook
1. Locate the Python code in `colab/colab_notebook.py`.
2. Create a new Google Colab notebook.
3. Copy-paste the script contents into a cell and run.
4. Paste a list of URLs (e.g. `["https://reluconsultancy.in", "stripe.com"]` or `https://reluconsultancy.in, stripe.com`) when prompted.
5. The notebook will write a local `results.json` file and print the formatted output array.

---

## Deployment Guide

### Backend: Render
1. Sign up on [Render.com](https://render.com).
2. Create a new **Web Service** connected to your repository.
3. Configure build parameters:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn core.wsgi:application --chdir backend` (Render will serve through gunicorn)
4. Add environment variables in Render's dashboard:
   - `GROQ_API_KEY`: Paste your key.
   - `DEBUG`: `False`
   - `SECRET_KEY`: Create a random secret key.

### Frontend: Vercel
1. Sign up on [Vercel](https://vercel.com).
2. Connect your repo and set:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add environment variables in Vercel:
   - `VITE_API_URL`: Use your Render Web Service live URL (e.g. `https://relu-enrichment.onrender.com`).
