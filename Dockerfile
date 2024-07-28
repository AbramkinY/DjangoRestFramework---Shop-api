FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD /app
RUN pip install --upgrade pip && pip install -r req.txt
