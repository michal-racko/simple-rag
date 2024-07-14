# Simple RAG

This project focuses on creation of a simple Retrieval-Augmented Generation
system based on open-source LLM models.

## Project structure

### Analysis

The `analysis` folder keeps track of the research conducted on individual parts
of the system. `analysis/experiments` contains Jupyther notebooks with
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

Experimental results are logged in the MLFLow db file. To view the results start
the MLFlow server and navigate to `localhost:5000`. Experiment are listed in the
top-left part of the UI. Experiment naming follows names of the corresponding
jupyther notebooks.