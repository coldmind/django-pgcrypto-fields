import datetime

from django.test import TestCase

from pgcrypto_fields import aggregates, proxy
from pgcrypto_fields import fields

from .factories import EncryptedModelFactory
from .models import EncryptedModel


EMAIL_PGP_FIELDS = (fields.EmailPGPPublicKeyField,)
PGP_FIELDS = EMAIL_PGP_FIELDS + (
    fields.IntegerPGPPublicKeyField,
    fields.TextPGPPublicKeyField,
    fields.DatePGPPublicKeyField,
)


class TestPGPMixin(TestCase):
    """Test `PGPMixin` behave properly."""
    def test_check(self):
        """Assert `max_length` check does not return any error."""
        for field in PGP_FIELDS:
            self.assertEqual(field(name='field').check(), [])

    def test_max_length(self):
        """Assert `max_length` is ignored."""
        for field in PGP_FIELDS:
            self.assertEqual(field(max_length=42).max_length, None)

    def test_db_type(self):
        """Check db_type is `bytea`."""
        for field in PGP_FIELDS:
            self.assertEqual(field().db_type(), 'bytea')


class TestEmailPGPMixin(TestCase):
    """Test emails fields behave properly."""
    def test_max_length_validator(self):
        """Check `MaxLengthValidator` is not set."""
        for field in EMAIL_PGP_FIELDS:
            field_validated = field().run_validators(value='value@value.com')
            self.assertEqual(field_validated, None)


class TestEncryptedTextFieldModel(TestCase):
    """Test `EncryptedTextField` can be integrated in a `Django` model."""
    model = EncryptedModel

    def test_fields(self):
        """Assert fields are representing our model."""
        fields = self.model._meta.get_all_field_names()
        expected = (
            'id',
            'email_pgp_pub_field',
            'integer_pgp_pub_field',
            'pgp_pub_field',
            'pgp_pub_date_field',
            'pgp_pub_null_boolean_field',
        )
        self.assertItemsEqual(fields, expected)

    def test_value_returned_is_not_bytea(self):
        """Assert value returned is not a memoryview instance."""
        EncryptedModelFactory.create()

        instance = self.model.objects.get()

        self.assertIsInstance(instance.email_pgp_pub_field, unicode)
        self.assertIsInstance(instance.integer_pgp_pub_field, int)
        self.assertIsInstance(instance.pgp_pub_field, unicode)

    def test_fields_descriptor_is_not_instance(self):
        """`EncryptedProxyField` instance returns itself when accessed from the model."""
        self.assertIsInstance(
            self.model.pgp_pub_field,
            proxy.EncryptedProxyField,
        )

    def test_value_query(self):
        """Assert querying the field's value is making one query."""
        expected = 'bonjour'
        EncryptedModelFactory.create(pgp_pub_field=expected)

        instance = self.model.objects.get()

        with self.assertNumQueries(0):
            instance.pgp_pub_field

    def test_value_pgp_pub(self):
        """Assert we can get back the decrypted value."""
        expected = 'bonjour'
        EncryptedModelFactory.create(pgp_pub_field=expected)
        instance = self.model.objects.get()
        value = instance.pgp_pub_field
        self.assertEqual(value, expected)

    def test_value_pgp_date_pub(self):
        """Assert we can get back the decrypted value."""
        expected = datetime.date.today()
        EncryptedModelFactory.create(pgp_pub_date_field=expected)

        instance = self.model.objects.get()
        value = instance.pgp_pub_date_field
        self.assertEqual(value, expected)

    def test_value_pgp_date_pub_null(self):
        """Assert we can get back the decrypted value."""
        EncryptedModelFactory.create(pgp_pub_date_field=None)
        instance = self.model.objects.get()
        self.assertIsNone(instance.pgp_pub_date_field)

    def test_value_pgp_null_boolean_pub(self):
        """Assert we can get back the decrypted values."""
        EncryptedModelFactory.create(pgp_pub_null_boolean_field=None)
        instance = self.model.objects.last()
        self.assertIsNone(instance.pgp_pub_null_boolean_field)

        EncryptedModelFactory.create(pgp_pub_null_boolean_field=True)
        instance = self.model.objects.last()
        self.assertTrue(instance.pgp_pub_null_boolean_field)

        EncryptedModelFactory.create(pgp_pub_null_boolean_field=False)
        instance = self.model.objects.last()
        self.assertFalse(instance.pgp_pub_null_boolean_field)

    def test_value_pgp_pub_multipe(self):
        """Assert we get back the correct value when the table contains data."""
        expected = 'bonjour'
        EncryptedModelFactory.create(pgp_pub_field='au revoir')
        created = EncryptedModelFactory.create(pgp_pub_field=expected)

        instance = self.model.objects.get(pk=created.pk)
        value = instance.pgp_pub_field

        self.assertEqual(value, expected)

    def test_instance_not_saved(self):
        """Assert not saved instance return the value to be encrypted."""
        expected = 'bonjour'
        instance = EncryptedModelFactory.build(pgp_pub_field=expected)
        self.assertEqual(instance.pgp_pub_field, expected)
        self.assertEqual(instance.pgp_pub_field, expected)

    def test_decrypt_annotate(self):
        """Assert we can get back the decrypted value."""
        expected = 'bonjour'
        EncryptedModelFactory.create(
            pgp_pub_field=expected,
        )

        queryset = self.model.objects.annotate(
            aggregates.PGPPublicKeyAggregate('pgp_pub_field'),
        )
        instance = queryset.get()
        self.assertEqual(instance.pgp_pub_field__decrypted, expected)

    def test_decrypt_filter(self):
        """Assert we can get filter the decrypted value."""
        expected = 'bonjour'
        EncryptedModelFactory.create(
            pgp_pub_field=expected,
        )

        queryset = self.model.objects.annotate(
            aggregates.PGPPublicKeyAggregate('pgp_pub_field'),
        )
        instance = queryset.filter(pgp_pub_field__decrypted=expected).first()
        self.assertEqual(instance.pgp_pub_field__decrypted, expected)

    def test_update_attribute_pgp_pub_field(self):
        """Assert pgp field can be updated through its attribute on the model."""
        expected = 'bonjour'
        instance = EncryptedModelFactory.create()
        instance.pgp_pub_field = expected
        instance.save()

        updated_instance = self.model.objects.get()
        self.assertEqual(updated_instance.pgp_pub_field, expected)

    def test_update_one_attribute(self):
        """Assert value are not overriden when updating one attribute."""
        expected = 'initial value'
        new_value = 'new_value'

        instance = EncryptedModelFactory.create(
            pgp_pub_field=expected,
        )
        instance.pgp_sym_field = new_value
        instance.save()

        updated_instance = self.model.objects.get()
        self.assertEqual(updated_instance.pgp_pub_field, expected)

    def test_pgp_int_public_key_negative_number(self):
        """Assert negative value is saved with an `IntegerPGPPublicKeyField` field."""
        expected = -1
        instance = EncryptedModelFactory.create(integer_pgp_pub_field=expected)

        self.assertEqual(instance.integer_pgp_pub_field, expected)

    def test_pgp_int_public_key_null_number(self):
        """Assert negative value is saved with an `IntegerPGPPublicKeyField` field."""
        expected = None
        instance = EncryptedModelFactory.create(integer_pgp_pub_field=expected)
        self.assertEqual(instance.integer_pgp_pub_field, expected)

    def test_null(self):
        """Assert `NULL` values are saved."""
        instance = EncryptedModel.objects.create()
        fields = self.model._meta.get_all_field_names()
        fields.remove('id')
        for field in fields:
            self.assertEqual(getattr(instance, field), None)
