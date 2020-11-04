# from celery import Celery


# def make_celery(app):
#     print("mi chiamo")
#     print(app.import_name)
#     celery = Celery(
#         app.import_name,
#         backend=app.config["CELERY_RESULT_BACKEND"],
#         broker=app.config["CELERY_BROKER_URL"],
#         include=["monolith.services.background.tasks"],
#     )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery
