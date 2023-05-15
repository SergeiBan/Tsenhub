from celery import shared_task
from parts.models import Part
from inquiries.models import Inquiry


@shared_task
def save_inquiry(inquiry_objs, seeker):
    print(inquiry_objs, seeker)
