import sys
import pytest
from tk3u8.cli.args_handler import ArgsHandler
from tk3u8.constants import Quality


@pytest.fixture
def args_handler():
    return ArgsHandler()


def test_parse_args_username_only(args_handler, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "testuser"])
    args = args_handler.parse_args()
    assert args.username == "testuser"
    assert args.quality == "original"
    assert args.proxy is None


@pytest.mark.parametrize("quality", [quality.value.lower() for quality in Quality])
def test_parse_args_all_quality_values(args_handler, monkeypatch, quality):
    monkeypatch.setattr(sys, "argv", ["prog", "testuser", "-q", quality])
    args = args_handler.parse_args()
    assert args.username == "testuser"
    assert args.quality == quality


def test_parse_args_with_proxy(args_handler, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "testuser", "--proxy", "127.0.0.1:8080"])
    args = args_handler.parse_args()
    assert args.username == "testuser"
    assert args.quality == "original"
    assert args.proxy == "127.0.0.1:8080"


@pytest.mark.parametrize("quality", [quality.value.lower() for quality in Quality])
def test_parse_args_all_options(args_handler, monkeypatch, quality):
    monkeypatch.setattr(sys, "argv", ["prog", "testuser", "-q", quality, "--proxy", "127.0.0.1:8080"])
    args = args_handler.parse_args()
    assert args.username == "testuser"
    assert args.quality == quality
    assert args.proxy == "127.0.0.1:8080"


def test_parse_args_invalid_quality(args_handler, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "testuser", "-q", "invalid"])
    with pytest.raises(SystemExit):
        ArgsHandler().parse_args()
