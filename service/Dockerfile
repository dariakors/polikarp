FROM python:3.7

WORKDIR /service

COPY . /service

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "service.py"]
