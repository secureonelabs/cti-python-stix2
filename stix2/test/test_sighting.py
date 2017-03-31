import datetime as dt

import pytest
import pytz

import stix2

from .constants import INDICATOR_ID, SIGHTING_ID, SIGHTING_KWARGS


EXPECTED_SIGHTING = """{
    "created": "2016-04-06T20:06:37Z",
    "id": "sighting--bfbc19db-ec35-4e45-beed-f8bde2a772fb",
    "modified": "2016-04-06T20:06:37Z",
    "sighting_of_ref": "indicator--01234567-89ab-cdef-0123-456789abcdef",
    "type": "sighting",
    "where_sighted_refs": [
        "identity--8cc7afd6-5455-4d2b-a736-e614ee631d99"
    ]
}"""

BAD_SIGHTING = """{
    "created": "2016-04-06T20:06:37Z",
    "id": "sighting--bfbc19db-ec35-4e45-beed-f8bde2a772fb",
    "modified": "2016-04-06T20:06:37Z",
    "sighting_of_ref": "indicator--01234567-89ab-cdef-0123-456789abcdef",
    "type": "sighting",
    "where_sighted_refs": [
        "malware--8cc7afd6-5455-4d2b-a736-e614ee631d99"
    ]
}"""


def test_sighting_all_required_fields():
    now = dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)

    s = stix2.Sighting(
        type='sighting',
        id=SIGHTING_ID,
        created=now,
        modified=now,
        sighting_of_ref=INDICATOR_ID,
        where_sighted_refs=["identity--8cc7afd6-5455-4d2b-a736-e614ee631d99"]
    )
    assert str(s) == EXPECTED_SIGHTING


def test_sighting_bad_where_sighted_refs():
    now = dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)

    with pytest.raises(ValueError) as excinfo:
        stix2.Sighting(
            type='sighting',
            id=SIGHTING_ID,
            created=now,
            modified=now,
            sighting_of_ref=INDICATOR_ID,
            where_sighted_refs=["malware--8cc7afd6-5455-4d2b-a736-e614ee631d99"]
        )

    assert str(excinfo.value) == "Invalid value for Sighting 'where_sighted_refs': must start with 'identity'."


def test_sighting_type_must_be_sightings():
    with pytest.raises(ValueError) as excinfo:
        stix2.Sighting(type='xxx', **SIGHTING_KWARGS)

    assert str(excinfo.value) == "Invalid value for Sighting 'type': must equal 'sighting'."


def test_invalid_kwarg_to_sighting():
    with pytest.raises(TypeError) as excinfo:
        stix2.Sighting(my_custom_property="foo", **SIGHTING_KWARGS)
    assert str(excinfo.value) == "unexpected keyword arguments: ['my_custom_property']" in str(excinfo)


def test_create_sighting_from_objects_rather_than_ids(malware):  # noqa: F811
    rel = stix2.Sighting(sighting_of_ref=malware)

    assert rel.sighting_of_ref == 'malware--00000000-0000-0000-0000-000000000001'
    assert rel.id == 'sighting--00000000-0000-0000-0000-000000000002'
