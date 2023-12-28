#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 22:10:54 2023

@author: goodman@devops.kyiv.ua
"""
import os
import sys
import logging
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

# =============================================================================
# initialize the app
# =============================================================================

app = Flask(__name__)

# =============================================================================
# initialize the database
# =============================================================================
Base = declarative_base()
db = SQLAlchemy(model_class=Base)

basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, 'project.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
db.init_app(app)

# =============================================================================
# initialize logging
# =============================================================================
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
log = logging.getLogger(__name__)

# =============================================================================
# handlers for frequent server errors
# =============================================================================


@app.errorhandler(404)
def not_found(e):
    log.warning(e)
    return render_template('error.html', code=404), 404


@app.errorhandler(500)
def internal_error(e):
    log.error(e)
    return render_template('error.html', code=500), 500

# =============================================================================
# Check health, for kubernetes
# =============================================================================


@app.route("/health", methods=['GET'])
def health():
    log.debug(f"GET /health, remote addr: {request.remote_addr}")
    return jsonify({"status": "ok", "code": 200}), 200


# =============================================================================
# Utils
# =============================================================================
def filter_alert(alerts: list, risk: str):
    result = []
    for alert in alerts:
        if alert["riskdesc"].split()[0].lower() == risk.lower():
            result.append(alert)
    return result
