FROM python:3.6

EXPOSE 5000

WORKDIR /multiplexer

COPY requirements.txt /multiplexer
RUN pip install -r requirements.txt


COPY . .
CMD python app.py
