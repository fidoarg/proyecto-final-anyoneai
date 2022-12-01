FROM python:3.10.6 as base

ADD requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/src/
ENV ALGORITHM=HS256
ENV JWT_SECRET_KEY=060b4cc4e1ccf551e131e0c495939514006d257a16aab75580b37d4b898eb237

ADD ./ /src/

WORKDIR /src

FROM base as test
RUN ["pytest", "-v", "/src/tests"]

FROM base as build
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
