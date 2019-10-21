import re

from django.forms.fields import CharField, ValidationError
from django.utils.translation import ugettext_lazy as _

MY_KAD_RE_HYPHENATED = re.compile(
    r'^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])-\d{2}-\d{4}$'
)
MY_KAD_RE = re.compile(
    r'^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{2}\d{4}$'
)
INVALID_PLACE_OF_BIRTH = [
    '00', '17', '18', '19', '20', '69', '70', '73', '80', '81', '94', '95',
    '96', '97'
]


class MyKadField(CharField):
    """
    A form field that validates input as a Malaysia MyKad number.

    Conforms to the YYMMDD-PB-###G or YYMMDDPB###G format
    More info: https://en.wikipedia.org/wiki/Malaysian_identity_card

    .. versionadded:: 3.0
    """

    default_error_messages = {
        'invalid': _('Invalid MyKad number.')
    }

    def __init__(self, hyphen=True, *args, **kwargs):
        self.hyphen = hyphen
        if self.hyphen:
            self.pattern = MY_KAD_RE_HYPHENATED
        else:
            self.pattern = MY_KAD_RE

        super().__init__(**kwargs)

    def clean(self, value):
        value = super().clean(value)

        if value in self.empty_values:
            return self.empty_value

        match = self.pattern.match(value)

        pb = value[7:9] if self.hyphen else value[6:8]
        if (not match) or (pb in INVALID_PLACE_OF_BIRTH):
            raise ValidationError(self.error_messages['invalid'])

        return value
