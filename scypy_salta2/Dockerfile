# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Fernando Bardelli <fernando@fliabardelli.com.ar>"
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# Instala Lib Solicitadas por Ariel
RUN mamba install --yes \
    'jupyterlab-language-pack-es-ES' \
    'matplotlib' \
    'matplotlib-inline' \
    'numpy' \
    'xlwt' \
    'xlutils' \
    'pyexcel' \
    'gif' \
    'rise' \
    'voila' \
    'xlrd' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"