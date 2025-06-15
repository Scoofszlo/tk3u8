import pytest

from tk3u8.core.helper import is_username_valid


@pytest.mark.parametrize(
    "username,expected",
    [
        # Valid usernames
        ("valid_user123", True),
        ("abc", True),
        ("a1_b2.c3", True),
        ("a" * 2, True),
        ("a_b.c1", True),
        ("ab", True),  # minimum length

        # Invalid usernames
        ("InvalidUser", False),      # contains uppercase
        ("user-name", False),        # contains dash
        ("user name", False),        # contains space
        ("user@name", False),        # contains special character
        ("a", False),                # too short
        ("", False),                 # empty
        ("a" * 25, False),           # too long
        (".", False),                # only period
        ("_", False),                # only underscore
        ("a!b#c$", False),           # mixed invalid characters
    ]
)
def test_is_username_valid(username, expected):
    assert is_username_valid(username) is expected
