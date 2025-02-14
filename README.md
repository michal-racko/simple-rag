# Simple RAG

This project focuses on creation of a simple Retrieval-Augmented Generation
system based on open-source LLM models.

## Usage

First, make sure to install dependencies:

```
pip install -r requirements.txt
```

This system connects to an ollama RESP API instance. Please refer
to https://github.com/ollama/ollama for details on how to install ollama
locally, pull and run its LLM models.

### environment

Following env variables can be set:

- `SIMPLE_RAG_TEST` - run in the debug mode, using the development server and an
  SQLite file / default: `false`
- `SIMPLE_RAG_SQLITE_DB_PATH` - path to the SQLite file if in development mode
  / default: `<project-root>/dev.db`
- `SIMPLE_RAG_MAX_QUESTIONS` - defines the limit on questions per conversation /
  default: 5
- `SIMPLE_RAG_EMBEDDING_URL` - ollama embedding API URL /
  default: `http://localhost:11434/api/embeddings`
- `SIMPLE_RAG_EMBEDDING_MODEL` - embedding model name /
  default: `mxbai-embed-large`
- `SIMPLE_RAG_LLM_URL` - ollama chat URL /
  default: `http://localhost:11434/api/chat`
- `SIMPLE_RAG_LLM_MODEL` - chat LLM model name / default: `llama3:8b`
- `SIMPLE_RAG_RUN_ID` - which chromadb to select, corresponds to `run_id` in
  MLFLow / default: `d46674dd-c854-4335-b986-1de579166728`
- `SIMPLE_RAG_SIMILARITY_THRESHOLD` - similarity threshold for ChromaDB search /
  default: 335

### development server

Run the following commands to start a development server using an SQLite
database file.

```
export SIMPLE_RAG_TEST=True
fastapi dev src/api/v1/app.py
```

Start a new conversation with the chatbot:

```
curl -X POST http://127.0.0.1:8000/conversations/ \
     -H "Content-Type: application/json" \
     -d '{"text": "Do you ship your products worldwide?"}'
```

Continue in a conversation:

```
curl -X PUT http://127.0.0.1:8000/conversations/<id: str> \
     -H "Content-Type: application/json" \
     -d '{"text": "Can I buy your products in the Czech Republic?"}'
```

## Project structure

### src

Contains source code for the application serving the QnA chatbot.

### Tests

Tests use the pytest framework (please refer to https://docs.pytest.org for more
details).

Run rests:

```
pytest -v tests
```

### Analysis

The `analysis` folder keeps track of the research conducted on individual parts
of the system. `analysis/experiments` contains jupyter notebooks with
individual experiments. Please use MLFlow to track results of different
approaches.

To start a locally-hosted MLFlow server execute the `start_mlflow.sh` script
in `analysis`:

```
chmod +x start_mlflow.sh
./start_mlflow.sh
```

Otherwise, please connect to an MLFlow server shared with other analysts.

#### Experiments

Environment used for these experiments can be setup using
the `requirements-analysis.txt` file:

```
pip install -r requirements-analysis.txt
```

- `001-prepare-data.ipynb`: Focuses on data preparation and parsing
- `002-retriever-country.ipynb`: Analyzes performance of different embeddings
  and similarity metrics for the retriever
- `003-general-questions.ipynb`: Estimates the optimal document distance
  threshold for distinguishing between country-specific and general questions
- `004-prompt-engineering.ipynb`: Manually testing prompts and a PoC of the RAG
  system

Experimental results are logged in the MLFLow db file. To view the results start
the MLFlow server and navigate to `localhost:5000`. Experiment are listed in the
top-left part of the UI. Experiment naming follows names of the corresponding
jupyter notebooks.