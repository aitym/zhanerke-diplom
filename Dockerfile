FROM python:3

WORKDIR /usr/src/app

RUN adduser -D worker
USER worker
WORKDIR /usr/src/app

COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker . .

COPY . .
