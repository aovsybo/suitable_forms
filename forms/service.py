import re
from collections import OrderedDict


def get_type(sting):
    date_regex = re.compile(r'\b(?:\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})\b')
    phone_regex = re.compile(r'\+{1}\d{1}\s{1}\d{3}\s{1}\d{3}\s{1}\d{2}\s{1}\d{2}')
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    if date_regex.match(sting):
        return "date"
    elif phone_regex.match(sting):
        return "phone"
    elif email_regex.match(sting):
        return "email"
    return "text"


def get_types(data: dict):
    data_types = {}
    for data_name, data_value in data.items():
        data_types[data_name] = get_type(data_value)
    return data_types


def convert_data(data: dict):
    return dict(eval(data["fields"]))
