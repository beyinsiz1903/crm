import re
from datetime import date
from decimal import Decimal, InvalidOperation
from fastapi import HTTPException


def field_key(field, index):
    if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]{0,63}', str(field.get('name', ''))):
        return field['name']
    label = str(field.get('label', '')).casefold()
    if field.get('type') == 'email':
        return 'email'
    if label in {'ad soyad', 'adınız soyadınız', 'name', 'isim'}:
        return 'name'
    if label in {'telefon', 'phone'}:
        return 'phone'
    if label in {'mesaj', 'message'}:
        return 'message'
    return f'field_{index}'


def validate_fields(schema, data):
    if not isinstance(data, dict) or len(data) > 100:
        raise HTTPException(422, 'Form verileri gecersiz')
    if data.get('website'):
        raise HTTPException(422, 'Gonderim reddedildi')
    result = {}
    for index, field in enumerate(schema):
        key = field_key(field, index)
        value = data.get(key, '')
        if not isinstance(value, (str, bool)):
            raise HTTPException(422, 'Form alanlari metin veya onay degeri olmali')
        value = value.strip() if isinstance(value, str) else value
        if field.get('required') and (value is False or not value):
            raise HTTPException(422, f'{field.get("label", key)} zorunlu')
        if len(str(value)) > 5000:
            raise HTTPException(422, 'Form alani cok uzun')
        if value and field.get('type') == 'email' and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', str(value)):
            raise HTTPException(422, 'E-posta adresi gecersiz')
        if field.get('type') == 'checkbox' and value not in {True, False, 'on', 'true', ''}:
            raise HTTPException(422, 'Onay degeri gecersiz')
        if value and field.get('type') == 'select':
            options = field.get('options', [])
            if isinstance(options, str):
                options = options.split(',')
            if value not in [str(option).strip() for option in options]:
                raise HTTPException(422, 'Secenek gecersiz')
        if value and field.get('type') == 'date':
            try:
                date.fromisoformat(str(value))
            except ValueError:
                raise HTTPException(422, 'Tarih gecersiz')
        if value and field.get('type') == 'number':
            try:
                if not Decimal(str(value)).is_finite():
                    raise InvalidOperation
            except InvalidOperation:
                raise HTTPException(422, 'Sayi gecersiz')
        result[key] = value
    return result


def validate_schema(schema):
    if len(schema) > 50:
        raise HTTPException(422, 'En fazla 50 form alani eklenebilir')
    keys = set()
    for index, field in enumerate(schema):
        key = field_key(field, index)
        if key in keys or not str(field.get('label', '')).strip():
            raise HTTPException(422, 'Form alanlari bos veya ayni isimli olamaz; benzersiz alan adlari girin')
        keys.add(key)
        if field.get('type') not in {'text', 'email', 'phone', 'tel', 'textarea', 'select', 'date', 'number', 'checkbox'}:
            raise HTTPException(422, 'Desteklenmeyen form alan turu')


CONTACT_FIELDS = [
    {'name': 'name', 'label': 'Ad Soyad', 'type': 'text', 'required': True},
    {'name': 'email', 'label': 'E-posta', 'type': 'email', 'required': True},
    {'name': 'subject', 'label': 'Konu', 'type': 'text'},
    {'name': 'message', 'label': 'Mesaj', 'type': 'textarea', 'required': True},
    {'name': 'consent', 'label': 'Iletisim onayi', 'type': 'checkbox', 'required': True},
]
