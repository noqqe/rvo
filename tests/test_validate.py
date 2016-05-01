#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rvo.validate import validate as validate
import datetime


def test_validate_pass(validation_item):
    assert validate(validation_item)

def test_validate_wrong_field(validation_item):
    del validation_item["content"]
    validation_item["contentXXX"] = "FOO"
    assert not validate(validation_item)

def test_validate_missing_field(validation_item):
    del validation_item["created"]
    assert not validate(validation_item)

def test_validate_missing_field_title(validation_item):
    del validation_item["title"]
    assert not validate(validation_item)

def test_validate_tags_is_not_list_int(validation_item):
    validation_item["tags"] = 12
    assert not validate(validation_item)

def test_validate_tags_is_not_list_str(validation_item):
    validation_item["tags"] = "string"
    assert not validate(validation_item)

def test_validate_categories_is_not_list_int(validation_item):
    validation_item["categories"] = 12
    assert not validate(validation_item)

def test_validate_categories_is_not_list_str(validation_item):
    validation_item["categories"] = "string"
    assert not validate(validation_item)

def test_validate_content_unicode(validation_item):
    validation_item["content"] = 'ÜÜÜÜÄÄÄÜÜ'
    assert validate(validation_item)

def test_validate_title_unicode(validation_item):
    validation_item["title"] = 'ÜÜÜÜÄÄÄÜÜ'
    assert validate(validation_item)

def test_validate_title_list(validation_item):
    validation_item["title"] = ["list"]
    assert not validate(validation_item)

def test_validate_content_list(validation_item):
    validation_item["content"] = ["list"]
    assert not validate(validation_item)

def test_validate_creatd_as_string(validation_item):
    validation_item["created"] = "2016-01-02"
    assert not validate(validation_item)

def test_validate_updated_as_string(validation_item):
    validation_item["updated"] = "2016-01-02"
    assert not validate(validation_item)
