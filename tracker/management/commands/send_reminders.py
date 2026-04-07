from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from tracker.models import Assignment


class Command(BaseCommand):
    help = "Send assignment reminder emails"

    def handle(self, *args, **kwargs):

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

Priority: {assignment.priority}

Please complete it before the deadline.
"""

            send_mail(
                subject,
                message,
                None,
                [assignment.user.email],
                fail_silently=False
            )

        self.stdout.write(self.style.SUCCESS("Reminder emails sent"))