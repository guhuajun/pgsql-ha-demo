FROM python:3-alpine

WORKDIR /app/                                               

RUN echo "https://mirrors.aliyun.com/alpine/v3.9/main/" > /etc/apk/repositories && \
    apk update && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install retry names psycopg2-binary sqlalchemy \                                
        --index-url http://mirrors.aliyun.com/pypi/simple/ \
        --trusted-host mirrors.aliyun.com                   
                                                            
COPY app.py .
                                                            
CMD ["python", "app.py"]
