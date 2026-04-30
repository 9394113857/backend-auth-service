# =====================================================
# ❌ GLOBAL ERROR HANDLERS
# =====================================================

from flask import jsonify


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "error": "Resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "success": False,
            "error": "Bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled Exception")
        return jsonify({
            "success": False,
            "error": "Something went wrong"
        }), 500
