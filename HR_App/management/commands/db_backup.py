import os
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Backup MySQL database to a SQL file'

    def handle(self, *args, **kwargs):
        db = settings.DATABASES['default']
        user = db['USER']
        password = db['PASSWORD']
        db_name = db['NAME']
        host = db.get('HOST', 'localhost')
        port = db.get('PORT', '3306')

        backup_dir = os.path.join(settings.BASE_DIR, 'db_backups')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

        dump_cmd = f"mysqldump -u {user} -p{password} -h {host} -P {port} {db_name} > \"{backup_file}\""

        os.system(dump_cmd)
        self.stdout.write(self.style.SUCCESS(f"Backup successful: {backup_file}"))
