import json
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from customer_service.commands import EmailCommand

class Command(BaseCommand):
    help = 'Registers an Avro schema with the Confluent Schema Registry.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Extract command-line arguments
        schema_registry_url = settings.CONFLUENT_SCHEMA_REGISTRY_URL

        # Define your Avro schema
        schema = EmailCommand.get_avro_schema()

        # Convert the schema to a JSON string format
        schema_str = json.dumps(schema)

        # Prepare the payload for the Schema Registry API
        payload = {
            "schema": schema_str
        }

        # Register the schema using the Schema Registry REST API
        try:
            response = requests.post(
                f"{schema_registry_url}/subjects/{settings.SEND_EMAIL_SCHEMA_SUBJECT}/versions",
                headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
                data=json.dumps(payload)
            )

            # Check the response status
            if response.status_code == 200:
                schema_id = response.json().get("id")
                self.stdout.write(self.style.SUCCESS(f"Schema registered successfully with ID: {schema_id}"))
            else:
                raise CommandError(f"Failed to register schema. Status code: {response.status_code}, Error: {response.text}")

        except requests.RequestException as e:
            raise CommandError(f"Request failed: {e}")