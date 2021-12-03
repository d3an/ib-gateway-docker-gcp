# This is the dockerfile for our Exch-Fetcher instance

# Shell can be run via docker run -it *hedgecheap1/mono_exc:tag*
FROM python:3.9-slim

LABEL maintainers="Dimitri Vasdekis <dvasdekis@gmail.com>,James Bury <jabury@uwaterloo.ca>"

# Set Env vars
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Toronto

# Python Env vars
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# Install any Python package requirements
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY src/ /tmp/src
CMD ["python","/tmp/src/run_tests.py"]
