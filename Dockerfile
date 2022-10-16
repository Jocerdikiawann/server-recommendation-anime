FROM python:slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install -r requirements.txt

COPY . /usr/src/app/
EXPOSE 3000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=3000"]