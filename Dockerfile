FROM python:3.6.13

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install python3-tk -y
RUN apt-get install git -y
RUN git clone https://github.com/nodefluxio/vortex.git
RUN git checkout drop-enforce
RUN pip install vortex/src/runtime[onnxruntime] 
RUN pip install -r requirements2.txt

EXPOSE 80

CMD ["/bin/bash"]