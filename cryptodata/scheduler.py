from apscheduler.schedulers.background import BackgroundScheduler
from .views import fetch_cryptocurrency_data, f20

def schedule_cryptocurrency_data_update():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: fetch_cryptocurrency_data(1000), 'interval', hours=1)
    scheduler.add_job(lambda: fetch_cryptocurrency_data(200), 'interval', minutes=6)
    scheduler.start()
