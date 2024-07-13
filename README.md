# Simple RAG

This project focuses on creation of a simple Retrieval-Augmented Generation
system based on open-source LLM models.

## Project structure

### analysis

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

Otherwise, please connect to an MLFlow server shared by other analysts.
