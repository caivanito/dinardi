# import celery
from celery import shared_task
from celery.signals import task_success, task_failure
from ballot.celery import app

from voting.models import VotingStatus

@app.task
def check_status():
    voting_status = VotingStatus.objects.first()
    if voting_status:
        if voting_status.is_past_close_time():
            voting_status.close = True
            voting_status.save()
            print("SE CIRRRA LA VOTACIÓN")
        else:
            print("LA VOTACIÓN SIGUE ABIERTA")