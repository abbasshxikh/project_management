from enum import Enum
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()

SITE_URL = current_site.domain


EMAIL_VERIFY_MESSAGE = {
    "subject": "Please confirm your email",
    "title": "Hello, FirstName,",
    "body": f"\nWe need to confirm that it's you,\n{SITE_URL}/accounts/activate/UID/TOKEN/ \nIf you did not register an account with us, please ignore or delete this email",
    "footer": "\nThank you",
}

SUCCESS_REGISTRATION_MESSAGE = {
    "subject": "Welcome to Project Management System",
    "title": "Hello, FirstName,",
    "body": f"\nWelcome to Project Management System,\n{SITE_URL}/accounts/login/ \nThank you",
}


class ConstantHelper:
    """return the constant value"""

    @classmethod
    def get_values(cls):
        """return list of values on constants"""
        return [constant.value for constant in cls]

    @classmethod
    def get_choices(cls):
        """return list of tuples for choices"""
        return [
            (constant.value, constant.name.title().replace("_", " "))
            for constant in cls
        ]


class NonEmployeeConstants(ConstantHelper, Enum):
    """Non Employee enumeration"""

    INTERN = "intern"
    CONTRACT_BASED = "contract_based"


class FileTypeConstants(ConstantHelper, Enum):
    """File Type enumeration"""

    IMAGE = "image"
    PPT = "ppt"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    OTHER = "other"


class StatusConstants(ConstantHelper, Enum):
    """Status enumeration"""

    CREATED = "created"
    STUCK = "stuck"
    WORKING = "working"
    DONE = "done"


class RatingConstants(ConstantHelper, Enum):
    """Rating enumeration"""

    AVERAGE = "0-3"
    GOOD = "3-5"
    VERY_GOOD = "5-8"
    EXCELLENT = "8-10"
