FROM python:3.10-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
WORKDIR /app
COPY . .

# Default test command
CMD ["sh", "-c", "python manage.py test --no-input --parallel"]