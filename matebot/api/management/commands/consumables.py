import json

from django.core.management import BaseCommand

from api import models


class Command(BaseCommand):
    help = "Command to import consumables from a json file"

    def add_arguments(self, parser):
        parser.add_argument("--path", action="store")

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR("Deleting all old consumables"))
        [x.delete() for x in models.ConsumableModel.objects.all()]
        with open(options["path"]) as fh:
            decoded = json.load(fh)
            if "consumables" not in decoded:
                raise ValueError
            if not isinstance(decoded["consumables"], dict):
                raise ValueError
            for name in decoded["consumables"]:
                consumable = decoded["consumables"][name]
                messages = []
                for message in consumable["messages"]:
                    messages.append(models.ConsumableMessageModel.objects.create(message=message).id)
                c = models.ConsumableModel.objects.create(
                    description=consumable["description"],
                    price=consumable["price"],
                    symbol=consumable["symbol"]
                )
                [c.messages.add(x) for x in messages]
                c.save()
                self.stdout.write(self.style.SUCCESS(f"Added consumable {name}"))
