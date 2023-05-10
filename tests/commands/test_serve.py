from click.testing import CliRunner
from pytest_mock import MockerFixture

from fastapi_template.commands import serve


def test_serve(mocker: MockerFixture):
    uvicorn_run = mocker.patch("uvicorn.run")
    runner = CliRunner()

    result = runner.invoke(serve.main)
    assert result.exit_code == 0
    uvicorn_run.assert_called_with(
        "fastapi_template.app:create_app",
        factory=True,
        host="0.0.0.0",
        uds=None,
        port=8000,
        reload=False,
        access_log=False,
        log_config=None,
    )

    result = runner.invoke(serve.main, ["--port", "123"])
    assert result.exit_code == 0
    uvicorn_run.assert_called_with(
        "fastapi_template.app:create_app",
        factory=True,
        host="0.0.0.0",
        uds=None,
        port=123,
        reload=False,
        access_log=False,
        log_config=None,
    )

    result = runner.invoke(serve.main, ["--path", "/tmp/foo.socket"])
    assert result.exit_code == 0
    uvicorn_run.assert_called_with(
        "fastapi_template.app:create_app",
        factory=True,
        host="0.0.0.0",
        uds="/tmp/foo.socket",
        port=8000,
        reload=False,
        access_log=False,
        log_config=None,
    )


def test_serve_help():
    runner = CliRunner()

    result = runner.invoke(serve.main, ["--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: serve [OPTIONS]")
