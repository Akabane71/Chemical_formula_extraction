from pymongo import MongoClient
from urllib.parse import quote_plus
from app.core.config import mongodb_settings

_client = None


def _build_mongo_uri() -> str:
    user = mongodb_settings.MONGODB_USER
    password = mongodb_settings.MONGODB_PASSWORD
    host = mongodb_settings.MONGODB_HOST
    port = mongodb_settings.MONGODB_PORT
    dbname = mongodb_settings.MONGODB_DBNAME
    if user and password:
        auth = f"{quote_plus(user)}:{quote_plus(password)}@"
        return f"mongodb://{auth}{host}:{port}/{dbname}?authSource=admin"
    return f"mongodb://{host}:{port}/{dbname}"


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(_build_mongo_uri())
    return _client


def get_pdf_results_collection():
    client = get_mongo_client()
    db = client[mongodb_settings.MONGODB_DBNAME]
    return db["pdf_results"]
