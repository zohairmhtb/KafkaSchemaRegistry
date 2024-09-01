import json
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from customer_service.commands import EmailCommand


class Command(BaseCommand):
    help = "List all the Avro schemas registered with the Confluent Schema Registry for a specific topic."

    def add_arguments(self, parser):
        parser.add_argument(
            '--topic',
            type=str,
            required=True,
            help='The Kafka topic name for which to list schemas'
        )

    def handle(self, *args, **options):
        # Extract command-line arguments
        topic = options['topic']

        # Construct the subject name for the schema (for both key and value)
        subjects = [f"{topic}-key", f"{topic}-value"]

        try:
            for subject in subjects:
                # Fetch all versions of the schema associated with the subject
                response = requests.get(f"{settings.CONFLUENT_SCHEMA_REGISTRY_URL}/subjects/{subject}/versions")

                if response.status_code == 200:
                    versions = response.json()
                    self.stdout.write(self.style.SUCCESS(f"Found {len(versions)} versions for subject '{subject}':"))

                    for version in versions:
                        # Fetch the schema details for each version
                        schema_response = requests.get(f"{settings.CONFLUENT_SCHEMA_REGISTRY_URL}/subjects/{subject}/versions/{version}")
                        if schema_response.status_code == 200:
                            schema_details = schema_response.json()
                            self.stdout.write(f"Version {version}: {schema_details['schema']}")
                        else:
                            self.stdout.write(self.style.WARNING(f"Failed to fetch details for version {version}: {schema_response.text}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Subject '{subject}' not found or no schemas associated. Status code: {response.status_code}"))

        except requests.RequestException as e:
            raise CommandError(f"Request failed: {e}")