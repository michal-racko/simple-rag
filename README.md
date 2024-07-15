# Simple RAG

This project focuses on creation of a simple Retrieval-Augmented Generation
system based on open-source LLM models.

## Project structure

### src

Contains source code for the application serving the QnA chatbot.

### Tests

Tests use the pytest framework (please refer to https://docs.pytest.org for more
details). First, make sure to install dev dependencies:

```
pip install -r requirements-dev.txt
```

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

These experiment had been done using locally-hosted ollama models. Please refer
to https://github.com/ollama/ollama for details on how to install ollama, pull
and its LLM models.

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