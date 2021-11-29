FROM python:3.9-slim-buster

RUN mkdir /fastapi

WORKDIR /fastapi

# Copy source code to working directory
COPY . /fastapi
ADD . /fastapi


# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

CMD ["python", "similarity_app.py"]