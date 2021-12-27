import argparse
import secrets
import string

from django.core.management import BaseCommand

from api import models


class Command(BaseCommand):
    help = "Command to create, update or delete an application"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("action", choices=["create", "update", "delete"])
        parser.add_argument("--id", action="store", dest="application_id")

    def handle(self, *args, **options):
        if (options["action"] == "update" or options["action"] == "delete") and not options["application_id"]:
            self.stdout.write(self.style.ERROR("You are missing --id"))
        app_id = options["application_id"]
        alphabet = string.ascii_letters + string.digits
        if options["action"] == "update":
            try:
                application = models.ApplicationModel.objects.get(id=app_id)
                application.token = "".join(secrets.choice(alphabet) for _ in range(128))
                application.save(force_update=True)
            except models.ApplicationModel.DoesNotExist:
                self.stdout.write(self.style.ERROR("There's no application with that id"))
        elif options["action"] == "delete":
            try:
                application = models.ApplicationModel.objects.get(id=app_id)
                application.delete()
            except models.ApplicationModel.DoesNotExist:
                self.stdout.write(self.style.ERROR("There's no application with that id"))
        elif options["action"] == "create":
            application = models.ApplicationModel.objects.create(
                token="".join(secrets.choice(alphabet) for _ in range(128))
            )
            self.stdout.write(self.style.SUCCESS("Application created successfully:"))
            self.stdout.write(f"ID: {application.id}")
            self.stdout.write(f"Token: {application.token}")
