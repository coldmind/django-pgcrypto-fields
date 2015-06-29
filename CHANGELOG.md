## v0.8.3.python2

* Fixed `DatePGPPublicKeyField` with nullable values

## v0.8.2.python2

* Simplified `NullBooleanPGPPublicKeyField` field

## v0.8.1.python2

* Added `NullBooleanPGPPublicKeyField` field

## v0.8.0.python2

* Added `DatePGPPublicKeyField` field

## v0.7.0.python2

Ported library to python2

## v0.7.0

* Make `get_placeholder` accepts a new argument `compiler`
* Fix buggy import to `Aggregate`

**Note: these changes have been done for django > 1.8.0.**

## v0.6.4

* Remove `MaxLengthValidator` from email fields.

## v0.6.3

* Avoid setting `max_length` on PGP fields.

## v0.6.2

* Allow/check `NULL` values for:
  `TextDigestField`;
  `TextHMACField`;
  `EmailPGPPublicKeyField`;
  `IntegerPGPPublicKeyField`;
  `TextPGPPublicKeyField`;
  `EmailPGPSymmetricKeyField`.
  `IntegerPGPSymmetricKeyField`.
  `TextPGPSymmetricKeyField`.

## v0.6.1

* Fix `cast`ing bug when sending negative values to integer fields.

## v0.6.0

* Add `EmailPGPPublicKeyField` and `EmailPGPSymmetricKeyField`.

## v0.5.0

* Rename the following fields:
  `PGPPublicKeyField` to `TextPGPPublicKeyField`;
  `PGPSymmetricKeyField` to `TextPGPSymmetricKeyField`;
  `DigestField` to `TextDigestField`;
  `HMACField` to `TextHMACField`.
* Add new integer fields:
  `IntegerPGPPublicKeyField`;
  `IntegerPGPSymmetricKeyField`.

## v0.4.0

* Make accessing decrypted value transparent. Fix bug when field had a string
representation of `memoryview` for PGP and keyed hash fields.

## v0.3.1

* Fix `EncryptedProxyField` to select the correct item.

## v0.3.0

* Access `PGPPublicKeyField`  and `PGPSymmetricKeySQL` decrypted values with
field's proxy `_decrypted`.
* Remove descriptor for field's name and raw value.

## v0.2.0

* Add hash based lookup for `DigestField` and `HMACField`.
* Add `DigestField`, `HMACField`, `PGPPublicKeyAggregate`, `PGPSymmetricKeyAggregate`.

## v0.1.0

* Add decryption through an aggregate class.
* Add encryption when inserting data to the database.
