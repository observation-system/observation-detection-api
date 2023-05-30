FROM python:3.10.6

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get -y install locales vim less libgl1-mesa-dev && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

EXPOSE 8000
ENV PORT 8000
ENV HOST "0.0.0.0"

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install youtube-dl==2021.1.3