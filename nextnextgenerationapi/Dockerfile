FROM python:3.10.13

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN apt-get purge -y curl && apt-get update && apt-get install -y curl \
  && apt-get install -y lsb-release \
  && curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
  && curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update --allow-unauthenticated --allow-insecure-repositories \
  && ACCEPT_EULA=Y apt-get install --allow-unauthenticated -y msodbcsql18 \
  && ACCEPT_EULA=Y apt-get install --allow-unauthenticated -y mssql-tools18 \
  && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
  && exec $SHELL \
  && pip install --no-cache-dir -r requirements.txt

COPY ./source .
COPY ./models ./models/

CMD [ "python", "./app.py" ]
