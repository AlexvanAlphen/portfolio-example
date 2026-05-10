# Base image
FROM python:3.12

# this updates dependencies, installs curl and 
# rm -rf /var removes files only necessary during installation
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

COPY ./requirements.txt .
RUN /root/.local/bin/uv pip install --system --no-cache -r requirements.txt

COPY test.py test.py
ENTRYPOINT ["python", "test.py"]


