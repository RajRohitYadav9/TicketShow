from main import celery 
from models import User, Bookings
from celery.schedules import crontab
from communication import send_email
import time 
from flask import render_template


# celery.conf.broker_url="redis://localhost:6379/1"
# celery.conf.result_backend="redis://localhost:6379/2"
# celery.conf.enable_utc=False
# celery.conf.timezone='Asia/Kolkata'





@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=10, minute=30),daily_reminder.s())
    sender.add_periodic_task(crontab(hour=8, minute=30, day_of_month='1'),monthly_enterTainment_report.s()) 


@celery.task()
def daily_reminder():
    users=User.query.all()  
    for u in users:
        booking=Bookings.query.filter_by(user_id=u.user_id).first()
        if not booking:
            send_email('pycelery@gmail.com',u.email,u.username,'This is reminder to visit ticketshow. Do not forget to check new shows added today')
            print("Sending reminder to:", u.username)
        


@celery.task()
def monthly_enterTainment_report():
    users=User.query.all()
    for u in users:
        bookings=Bookings.query.filter_by(user_id=u.user_id).all()
        mer=render_template('monthly_entertainment_report.html', user=u, bookings=bookings)
        send_email('pycelery@gmail.com',u.email,u.username,'Check out your monthly entertainment report', mer)
        print('sending report to ', u.email)


