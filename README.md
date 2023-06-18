# Data mapper project

Sandbox project to trial DDD using SQLAlchemy to provide the data mapper
pattern.

## Getting started

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

Run tests with:

```sh
py.test
```
