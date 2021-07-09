#Dockerfile

FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install uvicorn fastapi aiofiles jinja2 requests

COPY . .

EXPOSE 5656
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5656"]
