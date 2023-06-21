# Data mapper project

Sandbox project to trial DDD using SQLAlchemy to provide the data mapper
pattern.

## Getting started

Create a Python 3.11 virtualenv and run:

```bash
make install
```

to install the local `talkfu` package and its dependencies from
`requirements.txt`.

Create a local PostgreSQL database with name `datamapper`:

```bash
createdb datamapper
```

Run a local HTTP server with:

```sh
make run
```

This will create the schema in a local PostgreSQL database (credentials defined
in `config.py`).

## Development

Run all formatting, linting, tests and Mypy with:

```bash
make check
```

Run only the tests with:

```sh
py.test
```
