FROM airflow:2.2.5

USER root
# GDAL env vars, compilation settings
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
RUN set -ex \
  # workaround to install openjdk: https://github.com/geerlingguy/ansible-role-java/issues/64
  && mkdir -p /usr/share/man/man1 \
  && apt-get update \
  && apt-get install -yqq --no-install-recommends \
        vim \
        gettext-base \
        openjdk-11-jre \
        wget \
        less \
        zip \
        unzip \
        groff \
        gdal-bin \
        libgdal-dev \
        gcc \
        g++ \
        gnupg \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN set -ex \
  && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip awscliv2.zip \
  && ./aws/install -i /usr/local/aws-cli -b /usr/local/bin \
  && rm -rf awscliv2.zip ./aws

USER airflow
# GDAL requires older version of setuptools otherwise use_2to3 fails
RUN pip install --upgrade pip
RUN pip install 'setuptools<58.0.0'
RUN pip install 'GDAL<3.0'

# install additional libs
COPY ./requirements.txt .

# Get back the latest setuptools and wheel
RUN pip install 'setuptools>=59.1.1,<59.7.0' wheel
RUN pip install -r requirements.txt
RUN pip install --upgrade requests

# add $AIRFLOW_HOME, dags dir and airflow_aac_v1 dir to PYTHONPATH
ENV PYTHONPATH=$AIRFLOW_HOME/:$AIRFLOW_HOME/dags:$AIRFLOW_HOME/

# keep a new line for apending dbt plugins in dev and prod
