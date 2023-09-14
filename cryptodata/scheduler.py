from apscheduler.schedulers.background import BackgroundScheduler
from .views import fetch_cryptocurrency_data

def schedule_cryptocurrency_data_update():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_cryptocurrency_data, 'interval', minutes=2)
    scheduler.start()
