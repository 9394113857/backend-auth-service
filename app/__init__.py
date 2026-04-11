import os
import json
import uuid
from flask import Flask, g, request

from .config import Config
from .extensions import db, migrate, jwt, cors


def get_build_info():
    try:
        path = os.path.join(os.getcwd(), "build_info.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "version": "unknown",
            "tag": "unknown",
            "commit": "unknown",
            "commit_short": "unknown",
            "commit_title": "unknown",
            "commit_body": "No details available",
            "commit_time": "unknown",
            "build_time_utc": "unknown",
            "build_time_ist": "unknown",
        }


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.before_request
    def req_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    @app.get("/")
    def health():
        info = get_build_info()
        body = info.get("commit_body") or "No details available"

        return {
            "status": "running",
            "tag": info.get("tag"),
            "version": info.get("version"),
            "commit_short": info.get("commit_short"),
            "commit": info.get("commit"),
            "title": info.get("commit_title"),
            "body": body,
            "commit_time": info.get("commit_time"),
            "build_time_utc": info.get("build_time_utc"),
            "build_time_ist": info.get("build_time_ist"),
        }

    return app