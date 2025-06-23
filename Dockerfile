FROM python:3.13.2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements /code/
RUN pip install -r requirements
COPY . /code/