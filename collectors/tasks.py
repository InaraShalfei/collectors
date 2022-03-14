from web_collectors.models import Collection
from web_collectors.watermark import watermark_image
from .celery import app


@app.task
def delayed_collection_watermark(collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection.photo = watermark_image(collection.photo)
    collection.save()
