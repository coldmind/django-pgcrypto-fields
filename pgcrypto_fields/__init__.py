from django.conf import settings


CAST_TO_TEXT = "nullif(%s, NULL)::text"

INTEGER_PGP_PUB_ENCRYPT_SQL = "pgp_pub_encrypt({}, dearmor('{}'))".format(
    CAST_TO_TEXT,
    settings.PUBLIC_PGP_KEY,
)

PGP_PUB_ENCRYPT_SQL = "pgp_pub_encrypt(%s, dearmor('{}'))".format(
    settings.PUBLIC_PGP_KEY,
)
