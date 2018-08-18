FROM resin/raspberry-pi-python

#switch on systemd init system in container
ENV INITSYSTEM on

# pip install python deps from requirements.txt
# For caching until requirements.txt changes
COPY ./requirements.txt /requirements.txt
RUN pip --version
RUN pip install -r /requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

CMD ["python", "src/run.py"]