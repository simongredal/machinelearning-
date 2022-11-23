FROM python:latest

WORKDIR /app/
COPY requirements.txt /app/
RUN /bin/bash -c "pip install -r requirements.txt"

COPY app.py .
COPY templates/index.html templates/
COPY tenDigits.h5 .

EXPOSE 8000
ENTRYPOINT /bin/bash -c "gunicorn -t 3600 -b 0.0.0.0:8000 app:app"
