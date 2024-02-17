import six
import string
from ckan.lib.navl.dictization_functions import Missing, Invalid
from ckan.common import _

from ckan.logic.validators import email_validator as default_email_validator

import logging

log = logging.getLogger(__name__)

MIN_PASSWORD_LENGTH = 8
MIN_LEN_ERROR = (
    'Your password must be {} characters or longer, and consist of: upper and lower case letters, '
    'at least 1 digit(s), at least 1 special character(s) and not contain the username'
)

def user_password_validator(key, data, errors, context):
    value = data[key]
    username = data[('name',)]

    if isinstance(value, Missing):
        pass  # Already handled in core
    elif not isinstance(value, six.string_types):
        raise Invalid(_('Passwords must be strings.'))
    elif value == '':
        pass  # Already handled in core
    else:
        rules = [
            any(x.isupper() for x in value),
            any(x.islower() for x in value),
            any(x.isdigit() for x in value),
            any(x in string.punctuation for x in value),
            username not in value
        ]
        log.debug(f"Password validation user:{username} rules:{rules}")
        if len(value) < MIN_PASSWORD_LENGTH or sum(rules) < 5:
            raise Invalid(_(MIN_LEN_ERROR.format(MIN_PASSWORD_LENGTH)))


def email_validator(value, context):

    value = default_email_validator(value, context)

    if any(x.isupper() for x in value):
        raise Invalid("Email address should not contain upper case characters")

    return value