from django import forms
from .models import UploadedFile
from .validators import validate_file_extension_spreadsheet


class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file', 'name')


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(validators=[validate_file_extension_spreadsheet])
