FROM ubuntu:latest
RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-full python3-protobuf python3-pycurl git nano
RUN git clone https://github.com/jakored1/bssid_locator.git /bssid_locator
WORKDIR /bssid_locator
ENTRYPOINT ["python3","./main.py"]
