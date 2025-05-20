FROM python:3.10-slim

# Install dependencies
WORKDIR /app
COPY . /app

# Upgrade pip and install packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port (Railway injects PORT env var)
ENV PORT=8000
EXPOSE $PORT

# Run the app
CMD ["pserve", "production.ini", "--server-name", "main"]
