FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Railway injects the PORT env var
ENV PORT=8000
EXPOSE $PORT

# Start Pyramid app
CMD ["pserve", "production.ini", "--server-name=main"]
