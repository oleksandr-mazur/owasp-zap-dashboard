#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:19:29 2023

"""
import json
import logging
import itertools
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound
from flask import render_template, jsonify, request, abort, request
from __init__ import db, app

from models import Target, Scan


log = logging.getLogger(__name__)


@app.route("/", methods=['GET'])
def dashboard():
    log.info(f"{request.method} {request.path}, remote addr: {request.remote_addr} {request.user_agent}")
    targets = db.session.execute(db.select(Target)).scalars().all()
    return render_template('dashboard.html', targets=targets), 200


@app.route("/target/<target>", methods=['GET'])
def taget(target):
    log.info(f"{request.method} {request.path}, remote addr: {request.remote_addr} {request.user_agent}")
    query = db.select(Target).filter_by(host=target)
    obj = db.session.execute(query).scalar_one_or_none()
    if obj is None:
        abort(404, description=f"Target not found /target/{target}")
    return render_template('target.html', target=obj), 200


@app.route("/scan/<int:scan_id>", methods=['GET'])
def scan(scan_id: int):
    log.info(f"{request.method} {request.path}, remote addr: {request.remote_addr} {request.user_agent}")
    scan = db.get_or_404(Scan, scan_id)
    return render_template('scan.html', scan=scan,
                           alerts=json.loads(scan.alerts)), 200


@app.route("/api", methods=['POST'])
def api():
    log.info(f"{request.method} {request.path}, remote addr: {request.remote_addr} {request.user_agent}")
    if request.method == "POST" and request.is_json:
        data = request.get_json()

        try:
            summary = {
                "high": 0,
                "medium": 0,
                "low": 0,
                "informational": 0,
                "false_positives": 0
                }
            target_status = {
                "last_scan": datetime.strptime(
                    data["@generated"], "%a, %d %b %Y %X"),
                "name": data["site"][0]["@name"],
                "host": data["site"][0]["@host"],
                "port": data["site"][0]["@port"],
                "ssl": bool(data["site"][0]["@ssl"]),
            }

            alerts = data["site"][0]["alerts"]
            for alert in alerts:
                risk = alert["riskdesc"].split()[0].lower()
                summary[risk] = summary[risk] + 1

            log.info(f"{request.method} {request.path}, {summary}, remote addr: {request.remote_addr} {request.user_agent}")
            log.info(f"{request.method} {request.path}, {target_status}, remote addr: {request.remote_addr} {request.user_agent}")

            host = target_status["host"]
            try:
                target = db.session.execute(db.select(Target).filter_by(host=host)).scalar_one()
                for key, value in itertools.chain(target_status.items(), summary.items()):
                    setattr(target, key, value)

            except NoResultFound:
                target = Target(**target_status, **summary)

            scan = Scan(
                version=data["@version"],
                generated=datetime.strptime(data["@generated"], "%a, %d %b %Y %X"),
                alerts=json.dumps(data["site"][0]["alerts"])
                )
            target.scan.append(scan)

            db.session.add(target)
            db.session.commit()
            log.info(f"{request.method} {request.path}, Successfully added scan, remote addr: {request.remote_addr} {request.user_agent}")

            return jsonify({"text": "ok", "status": "ok", "code": 200}), 200
        except KeyError as error:
            log.exception(error)
        except Exception as error:
            log.exception(error)
            return jsonify({"text": "Internal error", "status": "error", "code": 500}), 500

    return jsonify({"text": "Bad request", "status": "error", "code": 400}), 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
