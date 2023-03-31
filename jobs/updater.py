from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import send_excercise

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_excercise, 'interval', hours=1)
    scheduler.start()

