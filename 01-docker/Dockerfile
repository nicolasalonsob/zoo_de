FROM python:3.12-slim

RUN pip install pandas sqlalchemy loguru psycopg2-binary pyyaml

WORKDIR /app

COPY config config
COPY pipeline.py pipeline.py 
COPY source_files source_files

ENTRYPOINT [ "python" , "pipeline.py"]
