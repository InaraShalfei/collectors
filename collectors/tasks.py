from web_collectors.watermark import watermark_image
from .celery import app


@app.task
def watermark_image(file):
    watermark_image(file)
