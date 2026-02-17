# Text to Indian Sign Language NLP

This is the Natural Language Processing (NLP) backend for converting English text into its Indian Sign Language (ISL) gloss representation.

## Features

- **Text Processing**: Tokenization and normalization using `spacy` and `nltk`.
- **ISL Grammar Mapping**: Converts English sentence structure to ISL grammar (rule-based).
- **Translation**: Supports Hindi and Marathi to ISL translation using `googletrans`.
- **API Endpoints**: Uses FastAPI to expose endpoints for the frontend.

## Key Files

*   **main.py**: The FastAPI application entry point.
*   **isl_nlp.py**: Core logic for mapping English sentence dependencies to ISL rules.
*   **code.py**: Utilities for sentence processing, reordering, and lemmatization.
*   **words.txt**: A list of valid words/vocabulary supported by the system (for checking against SigML files).

## Setup and Usage

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Server**:
    The server runs on port `3002`.

    ```bash
    python main.py
    ```

    Alternatively:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 3002 --reload
    ```

3.  **API Endpoints**:
    - **POST `/api`**: Accepts input text and returns the final response (processed ISL gloss).
    - **POST `/isl-text`**: Translates English text to ISL gloss.
    - **POST `/translate`**: Translates Hindi text to English, then to ISL.
    - **GET `/Hindi`**: Translates Hindi text to English.
    - **GET `/ToMarathi/{marathi_text}`**: Translates Marathi text to English.

## Dependencies

- **FastAPI**: Web framework.
- **spaCy**: NLP library (`en_core_web_sm` model required).
- **NLTK**: Natural Language Toolkit.
- **googletrans**: Translation APIs.

**Note**: You may need to download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```
