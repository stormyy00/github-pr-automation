from flask import jsonify


class Health:
    def health_check():
        return jsonify({"status": "healthy"})