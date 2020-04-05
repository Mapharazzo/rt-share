FROM python:3.6

EXPOSE 5000

WORKDIR /db_admin

COPY requirements.txt /db_admin
RUN pip install -r requirements.txt


COPY . .
CMD python db_interface.py
