from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from django.http import HttpRequest, HttpResponse
import json
from typing import List
from .commands import EmailCommand


from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry.error import SchemaRegistryError


# Create the configuration for Schema registry. Use Avro as the schema definition format
schema_registry_client = SchemaRegistryClient(settings.SCHEMA_REGISTRY_CONF)
avro_serializer = AvroSerializer(schema_registry_client, json.dumps(EmailCommand.get_avro_schema()), EmailCommand.parse_from_schema)
string_serializer = StringSerializer('utf_8')

# Create the producer instance
producer = Producer({'bootstrap.servers': settings.KAFKA_BROKER_URL})



def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

def send_command(data: dict):
    """
    This function receives a dictionary with the data from the form. It creates a message object and validates the schema agains the registry. 
    It then sends the message to the Kafka topic.
    @param data: dict
    @return: Tuple[str, bool]
    """
    # Convert the dictionary to message object
    command = EmailCommand.from_json(data)
    if command is None:
        return "Invalid command"

    response = "Email sent successfully"
    is_success = True
    try:
        # Validate the schema and send message to Kafka topic
        producer.produce(
            settings.KAFKA_EMAIL_TOPIC, 
            key=command.category, 
            value=avro_serializer(EmailCommand.to_json(command), SerializationContext(command.category, MessageField.VALUE)),
            on_delivery=delivery_report
        )
        producer.flush()
    except SchemaRegistryError as e:
        # If the schema is invalid, the message will not be sent
        print(f"Failed to send email: {e}")
        response = e.error_message
        is_success = False

    except Exception as e:
        print(f"Failed to send email: {e}")
        response = "Failed to send email"
        is_success = False
        raise ValueError(e)
    return response, is_success


def home(request: HttpRequest) -> HttpResponse:
    response, is_success = "Failed to send email", False
    if request.method == 'POST':
        response, is_success =send_command(request.POST)

    if request.method == "GET":
        response = None
    return render(request, 'customer_service/home.html', {'response': response, 'categories': EmailCommand.get_categories(), 'is_success': is_success})