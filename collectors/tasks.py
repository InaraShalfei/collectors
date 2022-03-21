from web_collectors.models import Collection, Photo, CollectionItem, Comment, \
    Follow
from web_collectors.send_message import send_message, notify_followers
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
def delayed_send_message_collection(collection_id):
    collection = Collection.objects.get(id=collection_id)
    text = (f'У автора {collection.owner} появилась '
            f'новая коллекция {collection.name}!')
    subject = 'Новая коллекция!'
    notify_followers(collection.owner, text, subject)


@app.task
def delayed_send_message_item(item_id):
    item = CollectionItem.objects.get(id=item_id)
    collection = item.collection
    text = (f'У автора {collection.owner} в коллекции {collection.name}'
            f' появился новый предмет {item.name}!')
    subject = f'Новый предмет из коллекции {collection.name}!'
    notify_followers(collection.owner, text, subject)


@app.task
def delayed_send_message_comment(comment_id):
    comment = Comment.objects.get(id=comment_id)
    subject = f'Новый комментарий'
    text = (f'Вашу коллекцию {comment.collection} '
            f'прокомментировал пользователь {comment.author}. '
            f'Текст комментария:{comment.text}')
    send_message(comment.collection.owner, text, subject)


@app.task
def delayed_send_message_reply_comment(reply_id):
    reply = Comment.objects.get(id=reply_id)
    subject = f'Новый комментарий'
    text = (f'На ваш комментарий "{reply.parent_comment}" '
            f'ответил пользователь {reply.author.username}. '
            f'Текст комментария:{reply.text}')
    send_message(reply.parent_comment.author, text, subject)


def delayed_send_message_follow(follow_id):
    follow = Follow.objects.get(id=follow_id)
    subject = f'Новая подписка'
    text = f'На вас подписался новый пользователь {follow.user}.'
    send_message(follow.author, text, subject)
