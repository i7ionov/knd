from iggndb.tests.base import BaseTest
from django.contrib.auth.models import Permission
from inspections.forms import InspectionForm
from dictionaries.models import Organization, User
import json
from inspections.models import Inspection
from datetime import datetime
from django.db import models
from mixer.backend.django import mixer


def create_inspections():
    mixer.cycle(5).blend(Inspection,
                         doc_number=mixer.FAKE,
                         doc_date=mixer.FAKE,
                         legal_basis__text=mixer.FAKE,
                         control_kind__text=mixer.FAKE,
                         control_form__text=mixer.FAKE,
                         control_plan__text=mixer.FAKE,
                         inspector__name=mixer.FAKE,
                         inspection_result__text=mixer.FAKE,
                         cancellation__text=mixer.FAKE,
                         date_begin=mixer.FAKE,
                         date_end=mixer.FAKE,
                         comment=mixer.FAKE,
                         act_date=mixer.FAKE)

