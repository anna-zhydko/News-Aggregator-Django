from news_agg.celery import app
from mainapp.rss_parser import get_trends


@app.task
def get_trends_task():
    return get_trends()
