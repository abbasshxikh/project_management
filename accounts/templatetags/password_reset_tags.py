from django import template
from accounts.constants import PASSWORD_RESET_EMAIL_MESSAGE

register = template.Library()


@register.simple_tag
def get_password_reset_message():
    password_reset_message = PASSWORD_RESET_EMAIL_MESSAGE
    return password_reset_message
