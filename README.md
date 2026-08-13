# AI Text Analyzer

An AI-powered text analysis application built with **Python, Google Gemini, and Streamlit**. The application analyzes user-provided text and generates a structured analysis containing a summary, key points, keywords, sentiment, entities, and actionable tasks.

## Features

* **AI-powered text summarization**
* **Key point extraction**
* **Keyword extraction**
* **Sentiment analysis**
* **Entity extraction**
* **Action-item extraction**
* **Long-text processing using chunking**
* **Multi-chunk result aggregation**
* **Structured JSON output**
* **Streamlit web interface**
* **Automated testing with Pytest**
* **Evaluation framework for model outputs**

## Architecture

```text
User Input
    │
    ▼
Streamlit Interface
    │
    ▼
Text Analyzer
    │
    ├── Short Text ──────► Gemini API
    │
    └── Long Text
            │
            ▼
       Text Chunking
            │
            ▼
       Gemini Analysis
            │
            ▼
     Chunk Result Aggregation
            │
            ▼
       Final Analysis
            │
            ▼
    Structured JSON Result
```

## Output

For each input, the application generates:

```json
{
  "summary": "Short summary of the text",
  "key_points": [
    "Important point 1",
    "Important point 2"
  ],
  "keywords": [
    "keyword 1",
    "keyword 2"
  ],
  "sentiment": "Neutral",
  "entities": [
    "Entity 1",
    "Entity 2"
  ],
  "action_items": [
    "Action item 1",
    "Action item 2"
  ]
}
```

## Tech Stack

* Python
* Google Gemini API
* Google GenAI SDK
* Streamlit
* Scikit-learn
* Pytest
* python-dotenv

## Project Structure

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
├── requirements.txt
├── run_gemini_test.py
├── run_long_text_test.py
└── streamlit_app.py
```

> `.env` is intentionally excluded from Git because it contains the Gemini API key.

## Installation

Clone the repository and move into the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-text-analyzer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit the `.env` file to GitHub.

## Run the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local URL where the application can be accessed.

## Long-Text Processing

The application handles large documents using a chunking strategy.

When the input exceeds the configured threshold:

```text
Large Document
      │
      ▼
Split into chunks
      │
      ├── Chunk 1 → Gemini
      ├── Chunk 2 → Gemini
      ├── Chunk 3 → Gemini
      └── ...
      │
      ▼
Combine chunk analyses
      │
      ▼
Final Gemini aggregation
      │
      ▼
Final structured analysis
```

This allows the application to process documents that are too large to analyze reliably in a single request.

## Testing

Run the automated tests:

```bash
python -m pytest
```

Current test suite:

```text
3 passed
```

The tests cover:

* Empty input validation
* Result structure validation
* Long-text processing

## Evaluation

The project includes an evaluation script:

```bash
python evaluate.py
```

The evaluation framework compares model predictions against predefined expected outputs.

Current benchmark:

| Metric                    |  Score |
| ------------------------- | -----: |
| Sentiment Accuracy        |    80% |
| Keyword Match             |    90% |
| Entity Match              |   100% |
| Action Item Match         |   100% |
| Summary TF-IDF Similarity | 42.89% |

The summary similarity score is based on lexical similarity and should **not** be interpreted as semantic summary accuracy.

The current benchmark contains only a small evaluation dataset, so these results should be treated as an initial project benchmark rather than statistically significant model performance.

## Example Use Cases

The application can be used for:

* Meeting notes analysis
* Business documents
* Customer feedback
* Product reviews
* Internal reports
* Project updates
* Task extraction
* Document summarization

## Key Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* LLM API integration
* Prompt engineering
* Structured JSON generation
* Text chunking
* Long-context processing
* Result aggregation
* Error handling
* Automated testing
* Model-output evaluation
* Streamlit application development
* Environment-variable management
* Git version control

## Limitations

* Analysis quality depends on the Gemini model response.
* LLM outputs can occasionally be inconsistent.
* The evaluation dataset is currently small.
* TF-IDF similarity does not measure semantic similarity perfectly.
* Long documents require multiple API calls, which can increase latency and API usage.

## Future Improvements

* Add semantic evaluation using embeddings.
* Add configurable Gemini model selection.
* Add document upload support for PDF and TXT files.
* Add caching to reduce repeated API calls.
* Add authentication.
* Add Docker support.
* Deploy the application to a cloud platform.
* Expand the evaluation dataset.
* Add logging and monitoring.

## License

This project is intended for educational and portfolio purposes.
