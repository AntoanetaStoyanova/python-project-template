import logging
from collections.abc import Iterator
from pathlib import Path

import pytest

from {{cookiecutter.project_slug}}.log import setup_logging


@pytest.fixture
def logger_name(request: pytest.FixtureRequest) -> Iterator[str]:
    name = f"test_log.{request.node.name}"
    yield name
    logger = logging.getLogger(name)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def test_setup_logging_sets_level(logger_name: str, tmp_path: Path) -> None:
    logger = setup_logging(logger_name, log_dir=tmp_path, level=logging.DEBUG)

    assert logger.level == logging.DEBUG


def test_setup_logging_writes_file(logger_name: str, tmp_path: Path) -> None:
    logger = setup_logging(logger_name, log_dir=tmp_path / "logs")
    logger.info("hello")

    log_files = list((tmp_path / "logs").glob(f"{logger_name}_*.log"))
    assert len(log_files) == 1
    assert "hello" in log_files[0].read_text(encoding="utf-8")
