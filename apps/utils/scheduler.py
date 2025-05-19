from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from apps.maintenance.models import MaintenanceSchedule, MaintenanceWarning
from apps.utils.send_telegram_message import send_telegram_message


def check_maintenance_warnings():
    # Get all MaintenanceSchedule objects that need warnings
    maintenance_schedules = MaintenanceSchedule.objects.all()

    for schedule in maintenance_schedules:
        # Check if the warning already exists
        warning = MaintenanceWarning.objects.filter(maintenance_schedule=schedule, is_sent=False).first()

        # If no warning exists, create one
        if not warning:
            warning = MaintenanceWarning.objects.create(maintenance_schedule=schedule)

        # Set warning time and level
        warning.set_warning_time()


        # Save the warning if it's due
        if warning.warning_time:
            warning.save()

            # Send a message to Telegram if it's not already sent
            if not warning.sent_to_telegram:
                send_telegram_message(warning.message)

                # Mark as sent
                warning.sent_to_telegram = True
                warning.sent_date = timezone.now()
                warning.save()


# Start function that schedules both jobs
def start():
    scheduler = BackgroundScheduler()

    # Schedule the maintenance warning check job every 24 hours
    scheduler.add_job(check_maintenance_warnings, 'interval', hours=3)
    # Start the scheduler
    scheduler.start()
