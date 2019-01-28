# Create your tasks here
from __future__ import absolute_import, unicode_literals
from iggndb.celery import app
from iggn_tools import excel
from iggndb import integration


@app.task
def import_from_gis_gkh(full=False):
    print('getting url and downloading')
    archive = integration.get_file_url(full)
    if archive is None:
        return
    print('unpacking' + archive)
    file = integration.unpack_zip(archive)
    if file is None:
        return
    print('importing inspections')
    excel.import_insp_from_gis_gkh(file)
    print('importing addresses')
    excel.import_addr_from_gis_gkh(file)
    print('importing orders')
    excel.import_order_from_gis_gkh(file)
    return 'import is complete'
