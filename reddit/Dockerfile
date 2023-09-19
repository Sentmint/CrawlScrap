FROM python:3.10-bullseye

ARG TO_DIR=/reddit_image

WORKDIR ${TO_DIR}

COPY .  ${TO_DIR}

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "reddit.py"]