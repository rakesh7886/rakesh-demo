FROM python:3.8-slim

WORKDIR /app

# # Install the dependencies
# RUN pip install --upgrade pip
# RUN pip install -r /app/requirements.txt

# Copy the requirements file
COPY ./requirements.txt requirements.txt

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy all the project files
COPY . .

# Expose the port and run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
