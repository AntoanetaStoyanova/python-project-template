import logging

import pytest

from {{cookiecutter.project_slug}}.__main__ import PROJECT_NAME, main


def test_main_logs_start(
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path_factory.mktemp("run"))
    logger = logging.getLogger(PROJECT_NAME)
    caplog.set_level(logging.INFO, logger=PROJECT_NAME)
    logger.addHandler(caplog.handler)

    main()

    assert f"Starting {PROJECT_NAME}" in caplog.messages
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
