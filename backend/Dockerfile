FROM python:3.11-slim

WORKDIR /app

# Copy dependency file first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application and config files into the working directory
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]