import os

DB_URL = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", "5432"),
    user=os.environ.get("DB_USER", ""),
    password=os.environ.get("DB_PASSWORD", ""),
    db_name=os.environ.get("DB_PASSWORD", "datamapper"),
)
