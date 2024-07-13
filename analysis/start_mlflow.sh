#!/bin/bash

# Starts a locally-hosted MLFlow server using an SQLite db located in
# the analysis directory

MLFLOW_DB_NAME=analysis.db

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mlflow server --backend-store-uri "sqlite:///$SCRIPT_DIR/$MLFLOW_DB_NAME"
