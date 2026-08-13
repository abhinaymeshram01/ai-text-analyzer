# 🤖 AI Text Analyzer

An AI-powered document analysis application that uses **Google Gemini** to analyze short and long text documents and extract structured insights such as summaries, key points, keywords, sentiment, named entities, and action items.

The application automatically handles long documents by splitting them into manageable chunks, analyzing each chunk independently, and combining the results into a final structured analysis.

## 🚀 Live Demo

**Streamlit App:** https://ai-text-analyzer-5zuuvd7fa5m7hsbvbt6j8g.streamlit.app/

**GitHub:**
https://github.com/abhinaymeshram01/ai-text-analyzer

---

## 📌 Project Overview

Reading and analyzing long documents manually can be time-consuming.

This project provides an AI-powered interface where users can upload a `.txt` document or paste text directly into the application.

The system sends the text to **Google Gemini**, extracts structured information, and presents the results through an interactive Streamlit dashboard.

### The application extracts:

* 📝 Summary
* 🔑 Key Points
* 🏷️ Keywords
* 😊 Sentiment
* 🏢 Named Entities
* ✅ Action Items

For long documents, the application automatically performs **chunk-based processing** instead of sending the entire document in a single request.

---

## ✨ Features

### 📝 Intelligent Summarization

Generate summaries in three modes:

* Short
* Medium
* Detailed

### 📚 Long Document Processing

Documents exceeding the configured threshold are automatically divided into smaller chunks.

Each chunk is analyzed independently and the results are combined into one final analysis.

### 🔑 Key Point Extraction

Identifies the most important information from the document.

### 🏷️ Keyword Extraction

Extracts important topics and terms from the document.

### 😊 Sentiment Analysis

Classifies the overall sentiment as:

* Positive
* Negative
* Neutral

### 🏢 Named Entity Extraction

Identifies relevant entities such as:

* Organizations
* Teams
* Locations
* Dates
* Other important named references

### ✅ Action Item Extraction

Identifies tasks, responsibilities, deadlines, and follow-up actions.

### 📊 Document Statistics

The Streamlit interface displays:

* Character count
* Word count
* Line count
* Paragraph count

### 📥 JSON Export

Analysis results can be downloaded as a structured JSON file.

### 🧪 Automated Testing

The project includes Pytest tests covering:

* Empty input validation
* Result structure
* Long-document processing

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │       User           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Streamlit Frontend  │
                         │ streamlit_app.py     │
                         └──────────┬───────────┘
                                    │
                         Text / TXT Upload
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Analyzer        │
                         │  app/analyzer.py     │
                         └──────────┬───────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                Short Text                    Long Text
                     │                             │
                     │                    ┌────────▼────────┐
                     │                    │  Text Chunking  │
                     │                    │   CHUNK_SIZE    │
                     │                    └────────┬────────┘
                     │                             │
                     │                       Multiple Chunks
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Prompts        │
                         │  app/prompts.py      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Gemini API        │
                         │ app/gemini_api.py    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Structured JSON      │
                         │ Response             │
                         └──────────┬───────────┘
                                    │
                          Long Text Only
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Result Combination   │
                         │ & Final Analysis     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Streamlit Results    │
                         │ Cards / Sections     │
                         └──────────────────────┘
```

---

# 🔄 Processing Pipeline

## 1. Input

The user can either:

* Upload a UTF-8 `.txt` file
* Paste text into the application

```text
TXT File / Text Input
        │
        ▼
   Input Validation
```

## 2. Document Classification

The analyzer checks the text length.

```text
Text
 │
 ├── <= 12,000 characters
 │        │
 │        ▼
 │    Direct Analysis
 │
 └── > 12,000 characters
          │
          ▼
      Chunk Processing
```

The current configuration uses:

```python
MAX_TEXT_LENGTH = 12000
CHUNK_SIZE = 8000
```

## 3. Chunking

For long documents, the system attempts to preserve paragraph boundaries.

```text
Long Document
      │
      ▼
Split into paragraphs
      │
      ▼
Create chunks
      │
      ├── Chunk 1
      ├── Chunk 2
      ├── Chunk 3
      └── ...
```

If an individual paragraph exceeds the chunk size, it is split into smaller pieces.

## 4. Gemini Analysis

Each chunk is passed through the prompt-building layer.

```text
Text Chunk
    │
    ▼
build_summary_prompt()
    │
    ▼
Gemini API
    │
    ▼
JSON Analysis
```

The expected structured output contains:

```json
{
    "summary": "...",
    "key_points": [],
    "keywords": [],
    "sentiment": "Neutral",
    "entities": [],
    "action_items": []
}
```

## 5. Result Combination

For long documents:

```text
Chunk 1 Analysis ─┐
Chunk 2 Analysis ─┤
Chunk 3 Analysis ─┤
Chunk 4 Analysis ─┤
                  ▼
           Combination Prompt
                  │
                  ▼
          Final Gemini Analysis
                  │
                  ▼
          Final Structured JSON
```

The final analysis removes duplicated information and combines related information.

## 6. Streamlit Presentation

The final JSON is parsed and displayed as separate UI sections:

```text
                    Analysis Result
                           │
       ┌───────────┬───────┼───────┬───────────┐
       ▼           ▼       ▼       ▼           ▼
    Summary    Key Points Keywords Sentiment Entities
                           │
                           ▼
                      Action Items
```

---

# 📁 Project Structure

```text
ai-text-analyzer/
│
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── gemini_api.py
│   └── prompts.py
│
├── data/
│   ├── evaluation_samples.json
│   ├── long_text.txt
│   └── sample.txt
│
├── test/
│   ├── __init__.py
│   └── test_analyzer.py
│
├── .env
├── .gitignore
├── evaluate.py
├── list_models.py
├── requirements.txt
├── run_gemini_test.py
├── run_long_text_test.py
├── streamlit_app.py
└── README.md
```

> `.env`, virtual environments, caches, and other sensitive/local files should remain excluded from Git.

---

# 🧩 Main Components

## `streamlit_app.py`

Responsible for the user interface.

Responsibilities:

* Text input
* TXT upload
* Summary length selection
* Document statistics
* Analyze button
* Result visualization
* JSON download
* Error handling

---

## `app/analyzer.py`

Contains the main document-analysis logic.

Responsibilities:

* Validate input
* Detect short vs. long documents
* Split long documents
* Analyze individual chunks
* Combine chunk-level results

Core functions include:

```python
split_text()
analyze_chunk()
summarize_text()
```

---

## `app/prompts.py`

Contains the prompt-building logic used to instruct Gemini.

This separates prompt design from the application and analyzer logic.

---

## `app/gemini_api.py`

Handles communication with Google Gemini.

Responsibilities:

* API key loading
* Gemini client creation
* Model invocation
* JSON response configuration
* API response handling

The application supports:

```text
Local Development
      │
      ▼
.env

Streamlit Cloud
      │
      ▼
Streamlit Secrets
```

The API key is never stored directly in the source code.

---

## `evaluate.py`

Evaluates the quality of the generated results against a manually created evaluation dataset.

The evaluation includes:

* Summary similarity
* Sentiment accuracy
* Keyword matching
* Entity matching
* Action-item matching

---

## `test/test_analyzer.py`

Contains automated tests for the analyzer.

Run:

```bash
python -m pytest
```

Example result:

```text
3 passed
```

---

# 🛠️ Tech Stack

### Programming Language

* Python

### AI / LLM

* Google Gemini

### Frontend

* Streamlit

### Data Processing

* JSON
* Python standard library

### Testing

* Pytest

### Environment Management

* python-dotenv

### API / SDK

* Google GenAI SDK

### Version Control

* Git
* GitHub

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/abhinaymeshram01/ai-text-analyzer.git
```

```bash
cd ai-text-analyzer
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit this file to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
venv/
__pycache__/
.pytest_cache/
```

---

# ▶️ Running the Application

Start Streamlit:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

# 🧪 Running Tests

Run the complete test suite:

```bash
python -m pytest
```

For detailed output:

```bash
python -m pytest -vv
```

---

# 📊 Evaluation

The project includes a small manually created evaluation dataset.

Current evaluation results:

| Metric             | Result |
| ------------------ | -----: |
| Sentiment Accuracy |    80% |
| Keyword Match      |    90% |
| Entity Match       |   100% |
| Action Item Match  |   100% |
| Summary Similarity | 42.89% |

### Important interpretation

These metrics should not be treated as a benchmark of Gemini's general performance.

The evaluation dataset is small, and the keyword/entity/action-item metrics use custom matching rules.

The summary similarity score is particularly limited because semantically equivalent summaries can use very different wording.

Therefore, the evaluation is primarily useful for **regression testing and checking whether changes to the application degrade structured output quality**.

---

# ⚠️ Limitations

* The application currently focuses on TXT documents.
* Gemini API usage depends on available API quota.
* LLM responses are probabilistic and may occasionally contain incorrect information.
* Long-document analysis requires multiple Gemini API calls.
* Chunk-based processing can lose context that exists across distant sections.
* Evaluation is based on a relatively small manually created dataset.
* Summary similarity does not fully measure semantic correctness.
* The application does not currently provide citation or source tracing for extracted information.

---

# 🔮 Future Improvements

Possible improvements include:

* [ ] PDF document support
* [ ] DOCX document support
* [ ] CSV analysis
* [ ] Larger evaluation dataset
* [ ] Better semantic evaluation using embedding similarity
* [ ] Source citations for extracted information
* [ ] Persistent analysis history
* [ ] User authentication
* [ ] Rate limiting
* [ ] Background processing for very large documents
* [ ] Docker deployment
* [ ] Cloud monitoring
* [ ] Automated CI/CD pipeline

---

# 🎯 What This Project Demonstrates

This project demonstrates practical experience with:

* LLM API integration
* Prompt engineering
* Structured JSON generation
* Long-document processing
* Text chunking
* Streamlit application development
* API-key management
* Error handling
* Automated testing
* LLM output evaluation
* Git/GitHub workflow
* Cloud deployment

---

# 👨‍💻 Author

**Abhinay Meshram**

GitHub:
https://github.com/abhinaymeshram01

---

## ⭐ Project Summary

**AI Text Analyzer** is an end-to-end LLM application that transforms unstructured documents into structured, actionable insights using Google Gemini, with automatic long-document chunking, evaluation, automated testing, and an interactive Streamlit interface.
