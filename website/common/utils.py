import datetime


def calculate_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_file_form_initial(file, ownership_check):
    return {'file': file.file, 'description': file.description, 'file_name': file.file.name, 'id': file.id,
            'ownership': ownership_check.id == file.uploaded_by.id}


# Ownership check can be a User, a Person, and Employee, etc. Just whatever you need based on attached files
def get_files_formset_initial(files_set, ownership_check):
    # Id is to find and delete the proper file if necessary. Ownership is for frontend styling.
    # Checks if you are able to delete a file
    return [{'file': file.file, 'description': file.description, 'file_name': file.file.name, 'id': file.id,
             'ownership': ownership_check.id == file.uploaded_by.id} for file in files_set.all()]
