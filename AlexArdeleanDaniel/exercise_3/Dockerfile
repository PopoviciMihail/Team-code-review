FROM python:3.11-slim

# Avoid generating .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY ../requirements.txt /app/requirements.txt

# Install python deps
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app files
COPY . /app

# Expose the default uvicorn port
EXPOSE 8000

# Use uvicorn to run the FastAPI app. The module path is exercise_3:app
CMD ["uvicorn", "exercise_3:app", "--host", "0.0.0.0", "--port", "8000"]
