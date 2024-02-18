# syntax=docker/dockerfile:1
FROM nginx:latest
WORKDIR  /usr/share/nginx/html 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["nginx", "app.py"]
