from django.conf import settings
from django.db import models

from pgcrypto_fields.mixins import PGPMixin


class PGPEncryptedManager(models.Manager):
    """Custom manager to decrypt values at query time."""

    use_for_related_fields = True

    def get_queryset(self, *args, **kwargs):
        """Django queryset.extra() is used here to add decryption sql to query."""
        select_sql = {}
        for f in self.model._meta.get_fields_with_model():
            field = f[0]
            if isinstance(field, PGPMixin):
                select_sql[field.name] = """pgp_pub_decrypt("{0}"."{1}", dearmor('{2}'))""".format(
                    field.model._meta.db_table, field.name, settings.PRIVATE_PGP_KEY,
                )
        return super(PGPEncryptedManager, self).get_queryset(*args, **kwargs).extra(select=select_sql)
