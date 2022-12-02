FROM python:3

WORKDIR /home/worker

RUN pip install --upgrade pip

ARG PUID=1000
ARG PGID=1000

RUN useradd -u ${PUID} worker && groupmod -o -g ${PGID} worker && usermod -o -u ${PUID} -g worker worker

COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker . .

USER worker
