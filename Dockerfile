FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PORT=8000
EXPOSE $PORT
 

COPY production.ini .
CMD ["pserve", "production.ini", "--server-name", "main"]
