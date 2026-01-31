from celery import shared_task
from django.utils import timezone

from .models import Reservation


@shared_task
def activate_todays_reservations():
    today = timezone.localdate()

    reservations = Reservation.objects.filter(
        status="confirmed",
        start_date=today,
    )

    for reservation in reservations:
        reservation.status = "active"
        reservation.save(update_fields=["status"])

    return reservations.count()


@shared_task
def complete_ended_reservations():
    today = timezone.localdate()

    reservations = Reservation.objects.filter(
        status="active",
        end_date=today,
    )

    for reservation in reservations:
        reservation.status = "completed"
        reservation.save(update_fields=["status"])

    return reservations.count()


@shared_task
def cleanup_expired_reservations():
    today = timezone.localdate()

    # Active and past end_date -> completed
    active_expired = Reservation.objects.filter(
        status="active",
        end_date__lt=today,
    )

    for reservation in active_expired:
        reservation.status = "completed"
        reservation.save(update_fields=["status"])

    # Pending/confirmed and past end_date -> cancelled
    pending_expired = Reservation.objects.filter(
        status__in=["pending", "confirmed"],
        end_date__lt=today,
    )

    for reservation in pending_expired:
        reservation.status = "cancelled"
        reservation.cancellation_date = timezone.now()
        reservation.cancellation_reason = "Auto-cancelled: end date passed"
        reservation.save(update_fields=["status", "cancellation_date", "cancellation_reason"])

    return {
        "completed": active_expired.count(),
        "cancelled": pending_expired.count(),
    }