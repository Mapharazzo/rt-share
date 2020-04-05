FROM python:3.6

EXPOSE 5000

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

CMD ["python", "/usr/src/app/db_interface.py"]