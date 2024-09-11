FROM asia-south1-docker.pkg.dev/q-gcp-01426-codex-cicd-24-08/codex-llms-package/dev:latest

# Set the working directory to /app
WORKDIR /app
RUN ls

# Copy the current directory contents into the container at /app
COPY ./src /app/
COPY ./requirements.txt /app/requirements.txt

# Install CURL for Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \ pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV GCP_PROJECT GCPProject
ENV APP_NAME AppName

# CMD exec uvicorn main:app --host 0.0.0.0 --timeout-keep-alive 1800 --port ${PORT}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--timeout-keep-alive", "1800","--port", "8080"]

# Healthcheck

HEALTHCHECK --interval=10s --timeout=5s CMD curl --fail http://0.0.0.0:8080/$APP_NAME/health || exit 1