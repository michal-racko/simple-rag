FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app

CMD ["fastapi", "run", "api/v1/app.py", "--port", "8000"]
