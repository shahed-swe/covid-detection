FROM python:3.8.10 
ENV PYTHONUNBUFFERED 1 
WORKDIR /diu 
ADD . /diu 
COPY ./requirements.txt /diu/requirements.txt
RUN python -m pip install --upgrade pip
RUN sudo apt-get install virtualenv && virtualenv env
RUN source env/bin/activate
RUN apt-get update && apt-get install -y python-opencv
RUN pip install -r requirements.txt
COPY . /diu
