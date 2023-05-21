
from celery import shared_task
from django.db import models
from .models import *
from django.utils import timezone
from datetime import datetime, timedelta


# celery task for Inactive the product only if it is registered before 2 months.
@shared_task()
def is_registered_before_two_months():
    two_months_ago = timezone.now() - timedelta(days=60)
    products_list = Productss.objects.filter(created_date__lt=two_months_ago.date())
    products_list.update(is_active=True)
