from __future__ import unicode_literals

import datetime

from django.db import models
from django.db.utils import six

from pgcrypto_fields import (
    INTEGER_PGP_PUB_ENCRYPT_SQL,
    PGP_PUB_ENCRYPT_SQL,
)
from pgcrypto_fields.mixins import (
    EmailPGPPublicKeyFieldMixin,
    PGPPublicKeyFieldMixin,
)


class EmailPGPPublicKeyField(EmailPGPPublicKeyFieldMixin, models.EmailField):
    """Email PGP public key encrypted field."""
    encrypt_sql = PGP_PUB_ENCRYPT_SQL


class IntegerPGPPublicKeyField(PGPPublicKeyFieldMixin, models.IntegerField):
    """Integer PGP public key encrypted field."""
    encrypt_sql = INTEGER_PGP_PUB_ENCRYPT_SQL

    @classmethod
    def _parse_decrypted_value(cls, value):
        if not isinstance(value, six.string_types):
            return value
        return int(value)


class TextPGPPublicKeyField(PGPPublicKeyFieldMixin, models.TextField):
    """Text PGP public key encrypted field."""
    encrypt_sql = PGP_PUB_ENCRYPT_SQL


class DatePGPPublicKeyField(PGPPublicKeyFieldMixin, models.DateField):
    """Date PGP public key encrypted field."""

    encrypt_sql = PGP_PUB_ENCRYPT_SQL

    @classmethod
    def _parse_decrypted_value(cls, value):
        if not isinstance(value, six.string_types):
            return value

        if value is None:
            return None
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()

    def get_prep_value(self, value):
        """
        Seem to be a bug in django==1.8.

        Need explicit string cast to avoid quotes.
        """
        if value is None:
            return None
        return "%s" % super(DatePGPPublicKeyField, self).get_prep_value(value)


class NullBooleanPGPPublicKeyField(PGPPublicKeyFieldMixin, models.NullBooleanField):
    """NullBoolean PGP public key encrypted field."""

    encrypt_sql = PGP_PUB_ENCRYPT_SQL

    def get_prep_value(self, value):
        """Before encryption, need to prepare values."""
        value = super(NullBooleanPGPPublicKeyField, self).get_prep_value(value)
        if value is None:
            return None
        return "%s" % bool(value)

    @classmethod
    def _parse_decrypted_value(cls, value):
        if not isinstance(value, six.string_types):
            return value

        if value == 'True':
            value = True
        elif value == 'False':
            value = False
        else:
            raise ValueError(
                'Unexpected returned value. '
                'Value: %s, type: %s' % (value, type(value))
            )
        return value
