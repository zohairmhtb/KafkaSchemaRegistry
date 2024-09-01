from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': settings.KAFKA_BROKER_URL})
from django.http import HttpRequest, HttpResponse
import json
from typing import List


class EmailCommand:
    def __init__(self, category:str, to:List[str], from_email:str, subject:str, body:str, is_html:bool=False):
        self.category = category
        self.to = to
        self.from_email = from_email
        self.subject = subject
        self.body = body
        self.is_html = is_html


    def to_json(self):
        return json.dumps({
            'to': self.to,
            'from_email': self.from_email,
            'subject': self.subject,
            'body': self.body,
            'isHtml': self.is_html,
            'category': self.category
        })

    @staticmethod
    def from_json(data:dict):
        return EmailCommand(
            to=data['to'],
            from_email=data['from_email'],
            subject=data['subject'],
            body=data['body'],
            is_html=data.get('is_html', False),
            category=data.get('category', '')
        )

def home(request: HttpRequest) -> HttpResponse:
    response = "Failed to send email"
    if request.method == 'POST':
        data = request.POST
        
        producer.produce(settings.KAFKA_EMAIL_TOPIC, key="1234", value=json.dumps(EmailCommand(
            to=[data.get('to', 'user@example.com')],
            from_email=data.get('from', 'admin@example.com').split(","),
            subject=data.get('subject', 'Welcome to our platform'),
            body=data.get('body', 'Welcome to our platform, we are happy to have you here!'),
            is_html=data.get('is_html', "False").lower() == "true",
            category=data.get('category', 'general')

        ).to_json()))
        producer.flush()
        response = "Email sent successfully"

    if request.method == "GET":
        response = None
    return render(request, 'customer_service/home.html', {'response': response})