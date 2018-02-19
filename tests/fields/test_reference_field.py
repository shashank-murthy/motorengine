#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from preggy import expect
from bson.objectid import ObjectId

from motorengine import Document, StringField, ReferenceField
from tests import AsyncTestCase


class User(Document):
    name = StringField()


class TestReferenceField(AsyncTestCase):
    def test_cant_create_reference_field_of_the_wrong_type(self):
        try:
            ReferenceField(reference_document_type=10).validate(None)
        except ValueError:
            err = sys.exc_info()[1]
            expected = "The field 'reference_document_type' argument must be a subclass of Document, not '10'."
            expect(err).to_have_an_error_message_of(expected)
        else:
            assert False, "Should not have gotten this far"

    def test_create_reference_field(self):
        field = ReferenceField(db_field="test", reference_document_type=User)
        expect(field.db_field).to_equal("test")
        expect(field.reference_type).to_equal(User)

    def test_create_reference_field_with_string_class(self):
        field = ReferenceField(db_field="test", reference_document_type="tests.fields.test_reference_field.User")
        expect(field.reference_type).to_equal(User)

    def test_to_son(self):
        field = ReferenceField(db_field="test", reference_document_type=User)

        u = User(name="test")
        u._id = ObjectId("123456789012123456789012")

        result = field.to_son(u)
        expect(str(result)).to_equal(str(u._id))
        expect(field.to_son(None)).to_equal(None)
        expect(field.to_son(u._id)).to_equal(u._id)

    def test_from_son(self):
        field = ReferenceField(db_field="test", reference_document_type=User)

        data = ObjectId("123456789012123456789012")

        result = field.from_son(data)

        expect(result).to_equal(ObjectId("123456789012123456789012"))

    def test_validate(self):
        field = ReferenceField(db_field="test", reference_document_type=User)
        expect(field.validate(None)).to_be_true()
        expect(field.validate("String")).to_be_false()
        expect(field.validate(ObjectId("123456789012123456789012"))).to_be_true()
