FROM python:3.6

EXPOSE 5000

WORKDIR /worker

COPY requirements.txt /worker
RUN pip install -r requirements.txt


COPY . .
CMD python app.py
