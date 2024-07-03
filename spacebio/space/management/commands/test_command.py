from django.core.management.base import BaseCommand
import logging

class Command(BaseCommand):
    help = 'Print a debug message to indicate the command was executed'

    def handle(self, *args, **kwargs):
        print("Debug message: The command was executed")
