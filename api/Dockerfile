FROM python:3.10.6 as base

ADD requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

#FROM base as test
#RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
