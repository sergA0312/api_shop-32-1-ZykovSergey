# Create your models here.
from datetime import datetime


def save_confirmation_code(user, code):
    user.confirmation_code = code
    user.confirmation_code_created_at = datetime.now()
    user.save()
