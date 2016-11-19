import pytest
import linkatos.message as message


# test url detection

def test_url_detection_of_https():
    expected = "https://example.org"

    assert message.extract_url("foo https://example.org") == expected


def test_detection_of_http():
    expected = "http://example.com"

    assert message.extract_url("foo http://example.com bar") == expected


def test_message_does_not_have_a_url():
    assert message.extract_url("foo htts://example.org") is None
