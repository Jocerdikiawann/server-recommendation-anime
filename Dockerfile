FROM python:3.8-slim-buster

WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/usr/src/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirment.txt /usr/src/app/
RUN pip3 install -r requirment.txt

COPY . /usr/src/app/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]