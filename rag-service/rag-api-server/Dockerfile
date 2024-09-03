# Python version
FROM python:3.9-slim

# having app as directory to workon -> copying requirements.txt
WORKDIR /code

# copying requirements.txt to docker container
COPY ./requirements.txt /code/requirements.txt

# upgrade pip and install requirements
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copying the rest
COPY ./app /code/app
COPY .env /code

# http
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]