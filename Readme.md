<p align="center">
  <img src="assets/images/logo.jpeg" alt="VIDHI>AI" width="150" height="150" style="border-radius: 20px;">
</p>

<h1 align="center">VIDHI.AI</h1>

<p align="center">
  <strong>AI-Powered Legal Assistant for Nepal</strong><br>
  <em>Making legal knowledge and government navigation accessible to every Nepali citizen.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/LLaMA_3.1-8B-purple?logo=meta" alt="LLaMA">
  <img src="https://img.shields.io/badge/FAISS-Vector_DB-green" alt="FAISS">
  <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi" alt="FastAPI">
 
</p>

---

##  Table of Contents

- [Table of Contents](#table-of-contents)
- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [1. Clone \& Install](#1-clone--install)
  - [2. Set API Key](#2-set-api-key)
  - [3. Run the App](#3-run-the-app)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Voice Input](#voice-input)
  - [API Usage](#api-usage)
- [API Reference](#api-reference)
  - [Base URL](#base-url)
  - [Endpoints](#endpoints)
    - [Query Legal Documents](#query-legal-documents)
    - [List Available Documents](#list-available-documents)
- [Demo Video](#demo-video)
- [Legal Documents Covered](#legal-documents-covered)
- [ Architecture](#️-architecture)
- [ Project Structure](#-project-structure)
- [FAQ](#faq)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
  - [Ways to Contribute](#ways-to-contribute)
  - [Commit Convention](#commit-convention)
- [Team](#team)
- [Acknowledgments](#acknowledgments)
  - [Resources \& References](#resources--references)
- [License](#license)
- [Why VIDHI.AI?](#why-vidhiai)

---

## Problem Statement

> Laws are easily accessible **but not easily understandable.**

For many Nepalis, one small paperwork mistake can cost a full day’s wage because the system is confusing, fragmented, and impossible to understand.

---

## Our Solution

**VIDHI.AI** is a conversational AI that lets anyone ask legal questions in plain language and get accurate, cited answers from **35+ Nepali laws and acts** and custom navigation data for Pokhara valley.

## How It Works

<p align="center">
  <img src="assets/images/workflow.png" alt="How it works" width="800">
</p>

---

## Key Features

| Feature                     | Description                                       |
| --------------------------- | ------------------------------------------------- |
| 1. **Natural Language Q&A** | Ask in English or Nepali, get clear answers       |
| 2. **35+ Legal Documents**  | Constitution, Civil Code, Criminal Code, and more |
| 3. **Source Citations**     | Every answer backed by actual legal text          |
| 4. **Procedure Navigation** | Step-by-step guidance for government services     |
| 5. **Voice Support**        | Speak your question, hear the answer              |
| 6. **Fast Retrieval**       | FAISS-powered vector search in milliseconds       |

---

## Tech Stack

| Layer          | Technology                           |
| -------------- | ------------------------------------ |
| **LLM**        | Meta LLaMA 3.1 8B (via HuggingFace)  |
| **Embeddings** | SentenceTransformers (MiniLM-L6)     |
| **Vector DB**  | FAISS                                |
| **Backend**    | FastAPI                              |
| **Frontend**   | React 18 + Vite / Streamlit          |
| **Voice**      | Edge TTS + Google Speech Recognition |

---

## Installation

### 1. Clone & Install

```bash
git clone https://github.com/GitWitAnish/Team-Pdf.git
cd Team-Pdf
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Create .env file
echo "HUGGINGFACE_API_KEY=your_key_here" > .env
```

### 3. Run the App

**FastAPI Backend:**

````bash
cd backend
python main.py ```

**React Frontend:**

```bash
cd frontend
npm run dev
````

Open **http://localhost:3000** for React UI

---

##  Usage

### Web Interface

1. Open the application in your browser
2. Type your legal question in the chat input
3. Wait for the AI to process and respond
4. View cited sources for verification

### Voice Input

1. Click the microphone icon
2. Speak your question clearly
3. The system will transcribe and process your query

### API Usage

```python
import requests

# Query the legal assistant
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "question": "What are my fundamental rights?",
        "language": "en",
        "max_sources": 8
    }
)

print(response.json())
```

---

##  API Reference

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

#### Query Legal Documents

```http
POST /query
```

| Parameter     | Type    | Required | Description                            |
| ------------- | ------- | -------- | -------------------------------------- |
| `question`    | string  | Yes      | The legal question to ask              |
| `language`    | string  | No       | Response language (`en` or `ne`)       |
| `max_sources` | integer | No       | Maximum sources to return (default: 8) |

**Response:**

```json
{
  "answer": "According to the Constitution of Nepal...",
  "sources": [
    {
      "document": "Constitution-of-Nepal(2072)",
      "section": "Part 3, Article 16",
      "relevance_score": 0.95
    }
  ],
  "processing_time": 1.23
}
```

#### List Available Documents

```http
GET /documents
```

**Response:**

```json
{
  "count": 35,
  "documents": [
    {
      "name": "Constitution of Nepal",
      "year": 2072,
      "category": "Constitutional"
    }
  ]
}
```

For complete API documentation, visit `/docs` when the server is running.

---

##  Demo Video



---

##  Legal Documents Covered

<details>
<summary><strong>Click to expand full list (35+ documents)</strong></summary>

**Constitutional**

- Constitution of Nepal (2072)
- National Civil Code (2074)
- National Penal Code (2074)
- National Criminal Procedure Code (2074)
- Sentencing Act (2074)
- Nepal Citizenship Act (2063)
- Nepal Citizenship (First Amendment) Act (2064)
- Nepal Citizenship (Second Amendment) Act (2079)

**Criminal Justice**

- Criminal Procedure Code (2074)
- Sentencing Code (2074)
- Prevention of Corruption Act (2059)
- Human Trafficking and Transportation (Control) Act (2064)
- Narcotic Drugs (Control) Act (2033)
- Arms and Ammunition Act (2019)
- Crime Victim Protection Act (2075)
- Evidence Act (2031)
- Prison Act (2019)

**Civil Rights**

- Citizenship Act (2063)
- Individual Privacy Act (2075)
- Right to Information Act (2064)
- Consumer Protection Act (2075)
- National Identity Card and Registration Act (2076)
- Birth, Death and Other Personal Events (Registration) Act (2033)
- Gender Equality Act (2063)
- Caste-based Discrimination and Untouchability (Offense and Punishment) Act (2068)

**Business**

- Company Act (2063)
- E-Commerce Act (2081)
- Income Tax Act (2058)
- Value Added Tax Act (VAT) (2052)
- Banking Offense and Punishment Act (2064)
- Foreign Investment and Technology Transfer Act (2075)
- Industrial Enterprises Act (2076)
- Securities Act (2063)
- Cooperative Act (2074)

**Social**

- Labour Act (2074)
- Education Act (2028)
- Domestic Violence (Crime and Punishment) Act (2066)
- Environment Protection Act (2076)
- Social Security Act (2075)
- Child Rights Act (2075)
- Senior Citizens Act (2063)
- Public Health Service Act (2075)
- Disability Rights Act (2074)
- Public Service Broadcasting Act (2049)

**Family & Personal Law**

- Marriage Registration Act (2028)
- Birth, Death and Other Personal Events (Registration) Act (2033)
- National Civil Code (2074) (Family Law Sections)
- Adoption Act (2018)

**Property & Land**

- Land Act (2021)
- Land Revenue Act (2034)
- Land Acquisition Act (2034)
- Guthi Act (2033)

**Other**

- Immigration Act (2049)
- Passport Act (2063)
- Motor Vehicle and Transport Management Act (2049)
- Public Procurement Act (2063)
- Press and Publication Act (2048)

</details>

---

##  Architecture

```
nyaya-exe/
├── streamlit/          #   Alternative UI
├── frontend/           #   React frontend 
├── backend/            #   FastAPI server
├── scripts/            #   Core RAG logic
│   ├── embedding.py    #   Text embeddings
│   ├── vector.py       #   FAISS operations
│   ├── llm_wrapper.py  #   LLaMA integration
│   └── voice.py        #   TTS/STT
├── database/           #   Vector index
└── dataset/            #   Legal documents
```

---

##  Project Structure

<details>
<summary><strong>Click to expand detailed structure</strong></summary>

```
vidhi-ai/
├── 📁 assets/
│   └── images/              # Logo, screenshots, diagrams
│   └── videos/ 
|
├── 📁 backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application entry
│   │   ├── core/            # Configuration and settings
│   │   ├── db/              # Database connections
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helper functions
│   ├── data/
│   │   ├── documents/       # Uploaded documents
│   │   └── faiss_index/     # Vector indexes
│   └── requirements.txt
│
├── 📁 database/
│   ├── legal_faiss.index    # FAISS vector index
│   └── legal_faiss_meta.json # Metadata for vectors
│
├── 📁 dataset/
│   ├── navigation/          # Government procedure data
│   ├── processed/           # Chunked legal documents
│   └── raw/                 # Original documents
│
├── 📁 frontend/
│   ├── public/              # Static assets
│   ├── src/                 # React components
│   ├── package.json
│   └── vite.config.js
│
├── 📁 notebooks/
│   └── main.ipynb           # Development notebooks
│
├── 📁 scripts/
│   ├── clean.py             # Data cleaning utilities
│   ├── embedding.py         # Text embedding generation
│   ├── llm_wrapper.py       # LLaMA integration
│   ├── navigation_processor.py
│   ├── vector.py            # FAISS operations
│   └── voice.py             # TTS/STT functionality
│
├── 📁 streamlit/
│   ├── streamlit.py         # Streamlit app
│   └── style.css            # Custom styling
│
├── .env                     # Environment variables
├── .gitignore
├── README.md
└── requirements.txt         # Python dependencies
```

</details>

---

##  FAQ

<details>
<summary><strong>Q: Is this legal advice?</strong></summary>

**A:** No. VIDHI.AI provides legal information, not legal advice. For specific legal matters, please consult a licensed attorney.

</details>

<details>
<summary><strong>Q: Which languages are supported?</strong></summary>

**A:** Currently, the system supports English and Nepali queries.

</details>

<details>
<summary><strong>Q: How accurate are the answers?</strong></summary>

**A:** Answers are generated based on actual legal documents with citations. However, users should verify critical information with official sources.

</details>

<details>
<summary><strong>Q: Can I add my own documents?</strong></summary>

**A:** Yes! Place PDF or TXT files in `dataset/raw/` and run the processing script:

```bash
python scripts/clean.py --input dataset/raw/ --output dataset/processed/
python scripts/vector.py --rebuild
```

</details>

<details>
<summary><strong>Q: Is my data private?</strong></summary>

**A:** Queries are processed through the HuggingFace API. For sensitive queries, consider running a local LLM instance.

</details>

---

##  Future Roadmap
- Full Nepali language support
- Analytics dashboard
- User authentication
- Mobile app (React Native)
- Integration with Nepal Law Commission
- Real-time document updates
- Lawyer consultation matching
- Document generation (legal templates)
- Multi-jurisdictional support

---

##  Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

-  **Report Bugs** - Open an issue describing the bug
-  **Suggest Features** - Share your ideas via issues
-  **Improve Documentation** - Help us write better docs
-  **Submit Code** - Fix bugs or implement features


### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Type       | Description           |
| ---------- | --------------------- |
| `feat`     | New feature           |
| `fix`      | Bug fix               |
| `docs`     | Documentation changes |
| `style`    | Code style changes    |
| `refactor` | Code refactoring      |
| `test`     | Adding tests          |
| `chore`    | Maintenance tasks     |


---

##  Team

<table>
  <tr>
    <td align="center">
      <strong>Milan Bastola</strong><br>
      <em>Full Stack Developer</em><br>
      <a href="https://github.com/Milan342">GitHub</a>
    </td>
    <td align="center">
      <strong>Prasanna Pahari</strong><br>
      <em>ML/AI Engineer</em><br>
      <a href="https://github.com/hopelessxD">GitHub</a>
    </td>
    <td align="center">
      <strong>Anish Karki</strong><br>
      <em>ML/AI Engineer</em><br>
      <a href="https://github.com/GitWitAnish">GitHub</a>
    </td>
  </tr>
</table>

---

##  Acknowledgments

We would like to thank:
- **Nepal Law Commission** - For making legal documents publicly available
- **Meta AI** - For the open-source LLaMA 3.1 model
- **HuggingFace** - For model hosting and inference API
- **FAISS Team** - For the efficient vector similarity search library
- **Sentence Transformers** - For pre-trained embedding models
- **Streamlit** - For the amazing data app framework
- **Open Source Community** - For all the libraries that made this possible

### Resources & References

- [Nepal Law Commission](https://lawcommission.gov.np/)
- [LLaMA Documentation](https://llama.meta.com/)
- [FAISS Documentation](https://faiss.ai/)

---

##  License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

##  Why VIDHI.AI?

1. **Solves a real problem** - Legal information gap in Nepal  
2. **Technically sound** - RAG architecture with state-of-the-art LLM  
3. **Scalable** - Easy to add more documents and languages  
4. **Accessible** - Voice support for low-literacy users  
5. **Open source** - Built for the community

---

<p align="center">
  <strong> Justice is everyone's right. (न्याय सबैको हक हो)</strong>
</p>

<p align="center">
  Made with ❤️ and Passion at <a href="https://hackathon-nova.com/">Hackathon Nova</a>  
</p>
