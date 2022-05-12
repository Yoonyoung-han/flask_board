# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /pybo
ENV FLASK_APP=pybo
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]