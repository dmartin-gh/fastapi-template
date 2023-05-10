import click
import os
import uvicorn


@click.command("serve")
@click.option("--path", metavar="PATH", help="Unix domain socket path")
@click.option("--port", type=int, default=8000, envvar="PORT", help="TCP port")
@click.option("-r", "--reload", is_flag=True, help="Enable auto-reload")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
def main(path: str, port: int, reload: bool, verbose: bool):
    """
    Run a uvicorn server instance listening on the given TCP port or unix
    domain socket path.
    """

    os.environ["VERBOSE"] = str(verbose).lower()

    uvicorn.run(
        "fastapi_template.app:create_app",
        factory=True,
        host="0.0.0.0",
        port=port,
        uds=path,
        reload=reload,
        access_log=False,
        log_config=None,
    )
