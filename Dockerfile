# syntax=docker/dockerfile:1

# Section 1- Base Image
FROM python:3.8-slim

# Section 2- Python Interpreter Flags
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Section 3- Compiler and OS libraries
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Section 4- Project libraries and User Creation
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt \
    && useradd -U peter \
    && install -d -m 0755 -o peter -g peter /app/core/static \
    && install -d -m 0755 -o peter -g peter /app/core/templates \
    && install -d -m 0755 -o peter -g peter /app/staticfiles

# Section 5- Code and User Setup
WORKDIR /app

USER peter:peter

COPY --chown=peter:peter . .

RUN chmod +x docker/*.sh

# Section 6- Expose port
EXPOSE 8000

# Section 7- Docker Run Checks, healthcheck and Configurations
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

ENTRYPOINT [ "docker/entrypoint.sh" ]
