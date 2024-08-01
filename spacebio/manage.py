#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time
from django.core.management import call_command

def start_jobs():
    time.sleep(5)
    call_command('start_jobs')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spacebio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
        
    # Start the job scheduler in a separate thread
    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
        threading.Thread(target=start_jobs).start()
        
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
