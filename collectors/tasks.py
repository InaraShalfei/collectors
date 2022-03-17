from web_collectors.models import Collection, Photo
from web_collectors.send_message import send_message
from web_collectors.watermark import watermark_image
from .celery import app


@app.task
def delayed_collection_watermark(collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection.photo = watermark_image(collection.photo)
    collection.save()


@app.task
def delayed_photo_watermark(photo_id):
    photo = Photo.objects.get(id=photo_id)
    photo.file = watermark_image(photo.file)
    photo.save()


@app.task
def delayed_send_message(collection_id):
    collection = Collection.objects.get(id=collection_id)
    for follower in collection.owner.followers.all():
        send_message(follower.user, collection)
