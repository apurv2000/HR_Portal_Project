from django.core.mail import EmailMessage
from django.conf import settings
from pathlib import Path
import zipfile
from datetime import datetime

def send_weekly_logs():
    log_dir = Path(settings.BASE_DIR) / 'logs' / 'users'
    zip_path = Path(settings.BASE_DIR) / 'logs' / f'employee_logs_{datetime.now().date()}.zip'

    # Create ZIP archive of all user logs
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for log_file in log_dir.glob('*.log'):
            zipf.write(log_file, arcname=log_file.name)

    # Send the ZIP via email
    email = EmailMessage(
        subject='Weekly Employee Logs',
        body='Attached are the weekly employee logs.',
        from_email=settings.EMAIL_HOST_USER,
        to=['apurvmalviya27@gmail.com', 'apurv.bvks@gmail.com'],
    )
    email.attach_file(zip_path)
    email.send()

    # Clear the logs after sending
    for log_file in log_dir.glob('*.log'):
        log_file.write_text('')
