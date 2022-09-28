FROM airflow:2.2.5

USER root
RUN set -ex \
    && apt-get update \
    && apt-get install -yqq --no-install-recommends vim

USER airflow
# install additional libs
COPY ./requirements.txt .
# COPY airflow_aac_v1 ./airflow_aac_v1
# add $AIRFLOW_HOME, dags dir and airflow_aac_v1 dir to PYTHONPATH
#ENV PYTHONPATH=$AIRFLOW_HOME/dags:$AIRFLOW_HOME/airflow_aac_v1
ENV PYTHONPATH=$AIRFLOW_HOME/:$AIRFLOW_HOME/dags:$AIRFLOW_HOME/airflow_aac_v1
RUN pip install --upgrade pip
RUN pip3 install --upgrade requests
RUN pip3 install -r requirements.txt
