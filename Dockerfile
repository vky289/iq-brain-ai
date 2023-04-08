# syntax=docker/dockerfile:1

FROM python:3

# Step 1: Install dependencies
# ----------------------------------------

RUN         apt-get update && apt-get install -y net-tools netcat

# Step 2: Install requirements.txt using pip
# ----------------------------------------

ENV         PYTHONUNBUFFERED=1
WORKDIR     /code
COPY        requirements.txt /code/
RUN         pip install -r requirements.txt

# Step 3: Copy Django Code
# ----------------------------------------

COPY        . /code/

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

CMD ["/code/runserver.sh"]