FROM python:3.10

WORKDIR /code

# Install Poetry
RUN pip install poetry

# Copy only the dependency definition files
COPY pyproject.toml poetry.lock* /code/

# Generate requirements.txt from Poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /code

# Run Alembic migrations
CMD ["alembic", "upgrade", "head"]

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:root", "--host", "0.0.0.0", "--port", "8000"]
