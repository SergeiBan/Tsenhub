from celery import shared_task
from parts.models import Part
from inquiries.models import Inquiry
from django.utils import timezone


@shared_task
def save_inquiry(inquiry_objs, seeker):
    this_moment = timezone.now()
    new_inquiries = [
        Inquiry(
            seeker_id=seeker, part=part['0'],
            amount=part['1'], inquiry_date=this_moment
        )
        for part in inquiry_objs
    ]
    Inquiry.objects.bulk_create(new_inquiries)