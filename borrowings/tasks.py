from celery import shared_task
from celery.utils.log import get_task_logger

from borrowings.models import Borrowing
from borrowings.send_telegram_message import send_telegram_message
from datetime import date, timedelta

logger = get_task_logger(__name__)


@shared_task()
def check_overdue_borrowings():
    tomorrow = date.today() + timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow,
        actual_return_date__isnull=True,
    )
    if overdue_borrowings.exists():
        for borrowing in overdue_borrowings:
            message = (
                f"Overdue borrowing num. {borrowing.id}\n"
                f"User: {borrowing.user.email}\n"
                f"Book: {borrowing.book.title}\n"
                f"Expected: {borrowing.expected_return_date}\n"
            )
            send_telegram_message(message)
    else:
        send_telegram_message("No overdue borrowings today!")
