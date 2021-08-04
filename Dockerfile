FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /zki
COPY requirements.txt /zki/
RUN pip install -r requirements.txt
COPY . /zki