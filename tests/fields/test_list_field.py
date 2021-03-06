#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from preggy import expect

from motorengine import ListField, StringField, Document, ReferenceField, EmbeddedDocumentField
from tests import AsyncTestCase


class TestListField(AsyncTestCase):
    def test_create_list_field(self):
        field = ListField(StringField(), db_field="test")
        expect(field.db_field).to_equal("test")
        expect(field._base_field).to_be_instance_of(StringField)

    def test_base_field_must_be_a_field(self):
        try:
            ListField("invalid", db_field="test")
        except ValueError:
            err = sys.exc_info()[1]
            expect(err) \
                .to_have_an_error_message_of("The list field 'field' argument must be an instance of BaseField, not 'invalid'.")
        else:
            assert False, "Should not have gotten this far"

    def test_to_son(self):
        field = ListField(StringField())

        expect(field.to_son([])).to_equal([])
        expect(field.to_son(["1", "2", "3"])).to_equal(["1", "2", "3"])

    def test_from_son(self):
        field = ListField(StringField())

        expect(field.from_son([])).to_equal([])
        expect(field.from_son(None)).to_equal([])
        expect(field.from_son(["1", "2", "3"])).to_equal(["1", "2", "3"])

    def test_validate_propagates(self):
        field = ListField(StringField())

        expect(field.validate(["1", "2", "3"])).to_be_true()
        expect(field.validate(["1", 2, "3"])).to_be_false()

    def test_validate_none(self):
        field = ListField(StringField())
        expect(field.validate(None)).to_be_true()

        field = ListField(StringField(), required=True)
        expect(field.validate(None)).to_be_false()

    def test_embedded_type(self):
        field = ListField(StringField())
        expect(field.item_type).to_equal(StringField)

    def test_item_reference_type(self):
        class OtherType(Document):
            pass

        field = ListField(ReferenceField(OtherType))
        expect(field.item_type).to_equal(OtherType)

    def test_item_embedded_type(self):
        class OtherType(Document):
            pass

        field = ListField(EmbeddedDocumentField(OtherType))
        expect(field.item_type).to_equal(OtherType)

    def test_to_query(self):
        field = ListField(StringField())
        field.from_son(["1", "2", "3"])
        expect(field.to_query(["1", "2", "3"])).to_equal({
            "$all": ["1", "2", "3"]
        })
        expect(field.to_query("string")).to_equal("string")

    def test_is_empty(self):
        field = ListField(StringField())
        expect(field.is_empty(None)).to_be_true()
        expect(field.is_empty([])).to_be_true()
        expect(field.is_empty("some")).to_be_false()
