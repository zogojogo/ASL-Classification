FROM python:3.6.13

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install python3-tk -y
RUN apt-get install git -y
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN git clone https://github.com/nodefluxio/vortex.git
RUN cd vortex && git checkout drop-enforce && pip install --ignore-installed --timeout=10000 ./src/runtime[onnxruntime]
RUN pip install -r requirements2.txt
RUN cd ~

EXPOSE 80

CMD ["/bin/bash"]