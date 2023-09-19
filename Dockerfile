FROM python:3.10-bullseye

ARG TO_DIR=/home/collectors

WORKDIR ${TO_DIR}

COPY /reddit/ ${TO_DIR}
COPY /stock ${TO_DIR}
COPY /twitter ${TO_DIR}
COPY /yahoo ${TO_DIR}
COPY requirements.txt ${TO_DIR}
COPY main.py ${TO_DIR}

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python", "main.py" ]