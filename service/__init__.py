"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS   # ✅ NEW

from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# 🔐 Security headers
talisman = Talisman(
    app,
    content_security_policy={
        "default-src": ["'self'"],
        "object-src": ["'none'"],
    },
    force_https=True,
)

# 🌐 CORS headers
CORS(app)   # ✅ THIS IS THE KEY LINE

# Import routes and models AFTER app creation
from service import routes, models  # noqa: E402,F401
from service.common import error_handlers, cli_commands  # noqa: E402,F401

# Logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")