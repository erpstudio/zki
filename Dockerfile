FROM python:3
ENV PYTHONUNBUFFERED=1
# RUN apt-get update && apt-get install -y \ 
# git \
# wget
RUN git clone https://github.com/erpstudio/zki.git
RUN  pip install -r zki/requirements.txt
RUN curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
# RUN docker-compose --version
RUN cd zki
RUN ls zki
RUN docker-compose up
# RUN cd zki


