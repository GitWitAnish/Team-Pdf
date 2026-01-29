<p align="center">
  <img src="assets/images/logo.jpeg" alt="VIDHI>AI" width="150" height="150" style="border-radius: 20px;">
</p>

<h1 align="center">VIDHI.AI</h1>

<p align="center">
  <strong>AI-Powered Legal Assistant for Nepal</strong><br>
  <em>Making legal knowledge and government navigation accessible to every Nepali citizen</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/LLaMA_3.1-8B-purple?logo=meta" alt="LLaMA">
  <img src="https://img.shields.io/badge/FAISS-Vector_DB-green" alt="FAISS">
  <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi" alt="FastAPI">
 
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-documentation">Documentation</a> •
  <a href="#-contributing">Contributing</a> 
  
</p>

---

## 📑 Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [How It Works](#-How-It-Works)
- [Key Features](#-key-features)
- [Tech Stack](#️-tech-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Demo](#-demo)
- [Legal Documents Covered](#-legal-documents-covered)
- [Architecture](#️-architecture)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [Team](#-team)
- [Acknowledgments](#-acknowledgments)
- [Support](#-support)

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

Open **http://localhost:5173** for React UI

---

## 📖 Usage

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
        "max_sources": 5
    }
)

print(response.json())
```

---

## 📡 API Reference

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
| `max_sources` | integer | No       | Maximum sources to return (default: 5) |

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

#### Health Check

```http
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "2h 30m"
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

## 📸 Demo

### Chat Interface

Ask any legal question and get instant, cited answers:

> **User:** "What are my fundamental rights according to Nepal's constitution?"
>
> **Nyaya.exe:** "According to the Constitution of Nepal (2072), you have 31 fundamental rights including:
>
> - Right to live with dignity (Article 16)
> - Right to freedom (Article 17)
> - Right to equality (Article 18)
> - Right to communication (Article 19)
>   ..."
>
> 📚 _Source: Constitution-of-Nepal(2072), Part 3_

---

## 📜 Legal Documents Covered

<details>
<summary><strong>Click to expand full list (35+ documents)</strong></summary>

**Constitutional**

- Constitution of Nepal (2072)
- National Civil Code (2074)
- National Penal Code (2074)

**Criminal Justice**

- Criminal Procedure Code (2074)
- Sentencing Code (2074)
- Prevention of Corruption Act (2059)

**Civil Rights**

- Citizenship Act (2063)
- Individual Privacy Act (2075)
- Right to Information (2064)
- Consumer Protection Act (2075)

**Business**

- Company Act (2063)
- E-Commerce Act (2081)
- Income Tax Act (2058)
- VAT Act (2052)

**Social**

- Labour Act (2074)
- Education Act (2028)
- Domestic Violence Act (2008)
- Environment Protection Act (2076)

_...and 15+ more_

</details>

---

## 🏗️ Architecture

```
nyaya-exe/
├── streamlit/          # 🖥️  Main UI (Streamlit app)
├── frontend/           # ⚛️  React frontend (alternative)
├── backend/            # 🔧 FastAPI server
├── scripts/            # 🧠 Core RAG logic
│   ├── embedding.py    #    Text embeddings
│   ├── vector.py       #    FAISS operations
│   ├── llm_wrapper.py  #    LLaMA integration
│   └── voice.py        #    TTS/STT
├── database/           # 📊 Vector index
└── dataset/            # 📚 Legal documents
```

---

## 📂 Project Structure

<details>
<summary><strong>Click to expand detailed structure</strong></summary>

```
vidhi-ai/
├── 📁 assets/
│   └── images/              # Logo, screenshots, diagrams
│
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
│   ├── streamlit.py         # Main Streamlit app
│   └── style.css            # Custom styling
│
├── .env                     # Environment variables
├── .gitignore
├── README.md
└── requirements.txt         # Python dependencies
```

</details>

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py          # Pytest fixtures
├── test_api.py          # API endpoint tests
├── test_embedding.py    # Embedding generation tests
├── test_vector.py       # FAISS operations tests
└── test_llm.py          # LLM integration tests
```

### Writing Tests

```python
# Example test
def test_query_endpoint(client):
    response = client.post(
        "/api/v1/query",
        json={"question": "What is Article 16?"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()
```

---

## 💬 FAQ

<details>
<summary><strong>Q: Is this legal advice?</strong></summary>

**A:** No. VIDHI.AI provides legal information, not legal advice. For specific legal matters, please consult a licensed attorney.

</details>

<details>
<summary><strong>Q: Which languages are supported?</strong></summary>

**A:** Currently, the system supports English queries with plans to add full Nepali language support in future updates.

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

<details>
<summary><strong>Q: Can I use this commercially?</strong></summary>

**A:** Please refer to the [License](#-license) section. The MIT license allows commercial use with proper attribution.

</details>

---

## 🔮 Future Roadmap

### Version 1.1 (Q2 2026)

- [ ] 🇳🇵 Full Nepali language support
- [ ] 📊 Analytics dashboard
- [ ] 🔐 User authentication

### Version 1.2 (Q3 2026)

- [ ] 📱 Mobile app (React Native)
- [ ] 🏛️ Integration with Nepal Law Commission
- [ ] 🔄 Real-time document updates

### Version 2.0 (Q4 2026)

- [ ] 🤝 Lawyer consultation matching
- [ ] 📄 Document generation (legal templates)
- [ ] 🌐 Multi-jurisdictional support

See the [open issues](https://github.com/your-team/nyaya-exe/issues) for a full list of proposed features.

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs** - Open an issue describing the bug
- 💡 **Suggest Features** - Share your ideas via issues
- 📖 **Improve Documentation** - Help us write better docs
- 🔧 **Submit Code** - Fix bugs or implement features

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/nyaya-exe.git
cd nyaya-exe

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git add .
git commit -m "feat: add amazing feature"

# Push and create a Pull Request
git push origin feature/amazing-feature
```

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

### Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Request review from maintainers

### Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## 👥 Team

<table>
  <tr>
    <td align="center">
      <strong>Member 1</strong><br>
      <em>Full Stack Developer</em><br>
      <a href="https://github.com/">GitHub</a>
    </td>
    <td align="center">
      <strong>Member 2</strong><br>
      <em>ML/AI Engineer</em><br>
      <a href="https://github.com/">GitHub</a>
    </td>
    <td align="center">
      <strong>Member 3</strong><br>
      <em>Backend Developer</em><br>
      <a href="https://github.com/">GitHub</a>
    </td>
    <td align="center">
      <strong>Member 4</strong><br>
      <em>UI/UX Designer</em><br>
      <a href="https://github.com/">GitHub</a>
    </td>
  </tr>
</table>

---

## 🙏 Acknowledgments

We would like to thank:

- **Meta AI** - For the open-source LLaMA 3.1 model
- **HuggingFace** - For model hosting and inference API
- **FAISS Team** - For the efficient vector similarity search library
- **Sentence Transformers** - For pre-trained embedding models
- **Nepal Law Commission** - For making legal documents publicly available
- **Streamlit** - For the amazing data app framework
- **Open Source Community** - For all the libraries that made this possible

### Resources & References

- [Nepal Law Commission](https://lawcommission.gov.np/)
- [Constitution of Nepal (English)](https://lawcommission.gov.np/en/?cat=17)
- [LLaMA Documentation](https://llama.meta.com/)
- [FAISS Documentation](https://faiss.ai/)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 VIDHI.AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 💪 Support

If you find this project helpful, please consider:

- ⭐ **Starring** the repository
- 🐦 **Sharing** on social media
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- ☕ **Buying us a coffee** - [Support Link]

---

## 🏆 Why VIDHI.AI?

✅ **Solves a real problem** - Legal information gap in Nepal  
✅ **Technically sound** - RAG architecture with state-of-the-art LLM  
✅ **Scalable** - Easy to add more documents and languages  
✅ **Accessible** - Voice support for low-literacy users  
✅ **Open source** - Built for the community

---

<p align="center">
  <strong>न्याय सबैको हक हो। Justice is everyone's right.</strong>
</p>

<p align="center">
  Made with ❤️ at [Hackathon Name]
</p>

<p align="center">
  <a href="#-table-of-contents">⬆️ Back to Top</a>
</p>
