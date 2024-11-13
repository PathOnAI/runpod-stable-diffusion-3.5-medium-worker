# Base image -> https://github.com/runpod/containers/blob/main/official-templates/base/Dockerfile
# DockerHub -> https://hub.docker.com/r/runpod/base/tags
FROM runpod/base:0.4.0-cuda11.8.0

# Add build argument
ARG HUGGINGFACE_TOKEN
# Set it as an environment variable
ENV HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN

COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

ADD src .

RUN python3.11 /handler.py

CMD python3.11 -u /handler.py
