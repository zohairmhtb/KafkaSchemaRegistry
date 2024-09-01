from __future__ import annotations
from typing import List
import json

class EmailCommand:
    GENERAL_EMAIL_CATEGORY = 'general'
    TECHNICAL_EMAIL_CATEGORY = 'technical'
    BILLING_EMAIL_CATEGORY = 'billing'

    def __init__(
        self, 
        category:str, 
        to:List[str], 
        from_email:str, 
        subject:str, 
        body:str, 
        is_html:bool=False,
        cc:List[str]=[],
        attachments:List[str]=[]
    ):
        self.category = category
        self.to = to
        self.from_email = from_email
        self.subject = subject
        self.body = body
        self.is_html = is_html
        self.cc = cc
        self.attachments = attachments


    @staticmethod
    def to_json(data:EmailCommand, *args, **kwargs):
        return json.dumps({
            'to': data.to,
            'from': data.from_email,
            'subject': data.subject,
            'body': data.body,
            'isHtml': data.is_html,
            'category': data.category,
            'cc': data.cc,
            'attachments': data.attachments
        })

    @staticmethod
    def to_json_from_string(data:str, *args, **kwargs):
        print(data)
        return json.loads(data)

    @staticmethod
    def from_json(data:dict, *args, **kwargs):
        cc = data.get('cc', '')
        to = data['to']
        attachments = data.get('attachments', '')
        return EmailCommand(
            to=to.split(',') if type(to) == str else to,
            from_email=data['from'],
            subject=data['subject'],
            body=data['body'],
            is_html=data.get('isHtml', False),
            category=data['category'],
            cc=data.get('cc', '').split(',') if type(cc) == str else cc,
            attachments=data.get('attachments', '').split(',') if type(attachments) == str else attachments
        )

    @staticmethod
    def parse_from_schema(data:str, *args, **kwargs):
        return EmailCommand.to_json_from_string(data)

    @staticmethod
    def get_categories():
        return {
            EmailCommand.GENERAL_EMAIL_CATEGORY: 'General',
            EmailCommand.TECHNICAL_EMAIL_CATEGORY: 'Technical',
            EmailCommand.BILLING_EMAIL_CATEGORY: 'Billing'
        }

    @staticmethod
    def get_avro_schema():
        return {
            'type': 'record',
            'name': 'EmailCommand',
            'fields': [
                {'name': 'to', 'type': {'type': 'array', 'items': 'string'}},
                {'name': 'from', 'type': 'string'},
                {'name': 'subject', 'type': 'string'},
                {'name': 'body', 'type': 'string'},
                {'name': 'isHtml', 'type': 'boolean'},
                {'name': 'category', 'type': 'string'},
                {'name': 'cc', 'type': {'type': 'array', 'items': 'string'}},
                {'name': 'attachments', 'type': {'type': 'array', 'items': 'string'}}
            ]
        }
