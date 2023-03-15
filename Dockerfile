FROM python:3.11-alpine

WORKDIR /bc-edu

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app .
COPY core .
COPY static .
COPY template .
COPY testcase .
COPY main.py .
COPY runtest.py .

CMD ["python", "main.py"]