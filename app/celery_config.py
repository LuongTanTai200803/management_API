from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )
    celery.conf.update(app.config.get('CELERY_CONFIG', {}))
    return celery