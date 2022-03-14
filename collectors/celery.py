import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# user = os.getenv('RABBITMQ_USERNAME')
# password = os.getenv('RABBITMQ_PASSWORD')
app = Celery('collectors',
             broker='amqp://localhost',
             include=['collectors.tasks'])

if __name__ == '__main__':
    app.start()
