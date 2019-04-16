# Create your tasks here
from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from iggndb.celery import app
from datetime import datetime
from inspections.models import Inspection, Precept


@app.task
def update_precept_days():
    query = Precept.objects.all()
    for p in query:
        p.update_days_to_start_new_inspection()
