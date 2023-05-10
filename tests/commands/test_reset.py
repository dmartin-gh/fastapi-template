from click.testing import CliRunner

from fastapi_template.commands import reset


def test_reset(postgres):
    runner = CliRunner()

    result = runner.invoke(reset.main)
    assert result.exit_code == 0


def test_reset_help():
    runner = CliRunner()

    result = runner.invoke(reset.main, ["--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: reset [OPTIONS]")
