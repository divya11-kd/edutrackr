from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Assignment


def send_assignment_reminders():

    tomorrow = timezone.now().date() + timedelta(days=1)

    assignments = Assignment.objects.filter(
        due_date=tomorrow,
        completed=False
    )

    for assignment in assignments:

        subject = "Assignment Reminder"

        message = f"""
Hello {assignment.user.username},

Reminder!

Your assignment "{assignment.name}" for subject "{assignment.subject}"
is due tomorrow ({assignment.due_date}).

Please complete it before the deadline.

Priority: {assignment.priority}

Thank you.
"""

        send_mail(
            subject,
            message,
            None,
            [assignment.user.email],
            fail_silently=False
        )