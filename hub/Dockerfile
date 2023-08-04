# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get install --yes locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "es_AR.UTF-8 UTF-8" > /etc/locale.gen 
    #locale-gen

# Configure environment
ENV LC_ALL=es_AR.UTF-8 \
    LANG=es_AR.UTF-8 \
    LANGUAGE=LANGUAGE=es_AR.UTF-8 \ 
    locale-gen=es_AR.UTF-8

# Install dockerspawner, nativeauthenticator
# hadolint ignore=DL3013

RUN python3 -m pip install --no-cache-dir \
    dockerspawner \
    jupyterhub-nativeauthenticator \
    

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
