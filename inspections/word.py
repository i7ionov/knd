from docxtpl import DocxTemplate
from inspections.models import Inspection
import jinja2

MONTH_NAMES = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря"]


def russian_date(date):
    format = "%d !B %Y"
    result = date.strftime(format)
    result = result.replace('!B', MONTH_NAMES[date.month - 1]) + 'г.'
    return result


def start():
    d = Inspection.objects.get(id=40812)
    doc = DocxTemplate('C:\\Users\\ivsemionov\\Desktop\\inspection.docx')

    context = {'doc': d}
    jinja_env = jinja2.Environment()
    jinja_env.filters['russian_date'] = russian_date
    doc.render(context, jinja_env)
    doc.render(context)
    doc.save("C:\\Users\\ivsemionov\\Desktop\\inspection1.docx")
