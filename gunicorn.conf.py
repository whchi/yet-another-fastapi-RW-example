from multiprocessing import cpu_count

from app.core.config import get_app_settings

settings = get_app_settings()

bind = '0.0.0.0:9999'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = cpu_count() * 2 - 1 if settings.APP_ENV == 'production' else 1
accesslog = '-'
errorlog = '-'
keepalive = 5
timeout = 120
loglevel = 'info' if settings.APP_ENV == 'production' else 'debug'
