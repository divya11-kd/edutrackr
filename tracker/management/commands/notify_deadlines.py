from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from tracker.models import Assignment
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send email notifications for upcoming assignment deadlines'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        upcoming_dates = [today + timedelta(days=1), today + timedelta(days=2)]

        assignments = Assignment.objects.filter(due_date__in=upcoming_dates, completed=False)

        for a in assignments:
            days_left = (a.due_date - today).days
            subject = f"Reminder: Assignment '{a.name}' due in {days_left} day(s)"
            message = f"Hi {a.user.username},\n\nYour assignment '{a.name}' for subject '{a.subject}' is due on {a.due_date}.\nPlease complete it on time.\n\nEduTrackr"
            recipient_list = [a.user.email]

            send_mail(subject, message, None, recipient_list)
            self.stdout.write(f"Notification sent for {a.name} due on {a.due_date}")