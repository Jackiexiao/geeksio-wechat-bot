# install: pip install "typer[all]" loguru
# usage:
#     python manage.py --help
#     python manage.py --install-completion

import os

import typer
from dotenv import load_dotenv

app = typer.Typer()


def run_cmd(cmd: str):
    os.system(cmd)


@app.command()
def install():
    run_cmd("pip install -r requirements.txt")


@app.command()
def init_db():
    run_cmd("python -m src.models")


@app.command()
def dev():
    load_dotenv(".env.dev")
    run_cmd("uvicorn src.main:app --reload --port 8011 --host 0.0.0.0")


@app.command()
def prd():
    load_dotenv(".env.prd")
    run_cmd("uvicorn src.main:app --port 8012 --host 0.0.0.0")


@app.command()
def client():
    run_cmd("python client.py")


@app.command()
def format_code():
    run_cmd("ruff check . --select I --fix")
    run_cmd("ruff format .")


if __name__ == "__main__":
    app()
