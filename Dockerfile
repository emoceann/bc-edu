FROM python:3.11-alpine

WORKDIR /bc-edu

COPY requirements.txt .
RUN pip install -r requirements.txt
#RUN pip install psycopg-binary

#COPY app .
#COPY core .
#COPY static .
#COPY template .
#COPY testcase .
#COPY main.py .
#COPY runtest.py .

COPY . .

CMD ["python", "main.py"]
