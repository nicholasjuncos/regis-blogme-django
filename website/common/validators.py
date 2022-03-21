import os
from django.core.exceptions import ValidationError


def validate_file_extension_pdf(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def validate_file_extension_spreadsheet(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv', '.xls', '.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
