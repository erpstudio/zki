FROM python:3.7
RUN  pip3 install virtualenv 
RUN virtualenv venv
RUN python3 -m venv /opt/venv
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR  /app/
RUN . /opt/venv/bin/activate 
RUN apt-get update 
COPY requirements.txt ./requirements.txt 
RUN  pip3 install -r ./requirements.txt 
COPY manage.py ./manage.py
COPY . .
EXPOSE 8000 
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
