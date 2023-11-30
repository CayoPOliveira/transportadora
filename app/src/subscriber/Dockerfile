FROM python:3.11
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
CMD ["uvicorn", "subscriber:app", "--host", "10.101.98.159", "--port", "8001", "--reload"]

