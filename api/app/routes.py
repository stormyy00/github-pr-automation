"""
routes.py specifies all the endpoints for the api
"""

from flask import Blueprint
from app.health.health import Health
from app.pullrequests.pullrequests import PRS
from app.reviewpr.reviewpr import Review
from app.mergepr.mergepr import Merge
from app.webhook.webhook import Webhook

main = Blueprint("main", __name__)


@main.route("/health", methods=["GET"])
def health():
    return Health().health_check(), 200

@main.route("/api/pull-requests", methods=["GET"])
def pullrequests():
    return PRS().list_prs(), 200

@main.route("/api/review-pr/<int:pr_number>", methods=["GET"])
def reviewpr(pr_number):
    return Review().review_pr(pr_number), 200

@main.route("/api/merge-pr/<int:pr_number>", methods=["POST"])
def mergepr(pr_number):
    return Merge().merge_pr(pr_number), 200

@main.route("/api/webhook", methods=["POST"])
def webhook():
    return Webhook().github_webhook(), 200
    