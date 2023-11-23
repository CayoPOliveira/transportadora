FROM python:3.11
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /code
CMD ["uvicorn", "api:app", "--host", "localhost", "--port", "8000", "--reload"]
