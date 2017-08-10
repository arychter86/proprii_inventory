from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, int_list_validator
from django.utils.translation import ugettext_lazy as _


numeric = int_list_validator(sep='-', message='Numeric characters separated by - allowed.', code='invalid', allow_negative=False)



def validate_tree_number(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not a positive integer'),
            params={'value': value},
        )

def validate_trunk(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not a positive integer'),
            params={'value': value},
        )
def validate_postive_int(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not a positive integer'),
            params={'value': value},
        )
