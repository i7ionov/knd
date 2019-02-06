from __future__ import absolute_import, unicode_literals
from iggndb.celery import app
from iggn_tools import excel
from iggndb import integration


@app.task
def generate_month_report():
    pass
