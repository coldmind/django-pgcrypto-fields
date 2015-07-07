from django.conf import settings
from django.db import models


from pgcrypto_fields.mixins import PGPMixin


class PGPEncryptedManager(models.Manager):
    """Custom manager to decrypt values at query time."""

    def get_queryset(self, *args, **kwargs):
        """Django queryset.extra() is used here to add decryption sql to query."""
        select_sql = {}
        encrypted_fields_names = []
        for f in self.model._meta.get_fields_with_model():
            if isinstance(f[0], PGPMixin):
                encrypted_fields_names.append(f[0].name)
        for field in encrypted_fields_names:
            select_sql[field] = "pgp_pub_decrypt({0}, dearmor('{1}'))".format(
                field, settings.PRIVATE_PGP_KEY,
            )
        qs = super(PGPEncryptedManager, self).get_queryset(*args, **kwargs)
        return qs.extra(select=select_sql)
