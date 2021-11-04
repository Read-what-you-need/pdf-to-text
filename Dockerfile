FROM python:3.9

LABEL maintainer="READ-NEED Core Maintainers <deeps@readneed.org>"

RUN apt-get update && apt install -y build-essential libpoppler-cpp-dev pkg-config python3-dev

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]