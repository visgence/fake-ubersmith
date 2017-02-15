FROM python:3.4-onbuild

EXPOSE 9131

RUN PBR_VERSION=0.0.0 pip install .

CMD fake-ubersmith
