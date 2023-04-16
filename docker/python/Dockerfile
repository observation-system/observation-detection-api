FROM python:3.10.6

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

EXPOSE 9000
ENV PORT 9000
ENV HOST "0.0.0.0"

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install youtube-dl==2021.1.3
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev