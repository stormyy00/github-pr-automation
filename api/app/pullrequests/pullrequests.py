from flask import jsonify

import logging
import requests
import json
from github import Github
from flask import Flask, request, jsonify
from ..config import repo


class PRS:
    @staticmethod
    def list_prs():
        try:
            pulls = repo().get_pulls(state="open")
            logging.info(f"✅ Retrieved {pulls.totalCount} open PRs.")
            return jsonify([{
                "number": pr.number, 
                "title": pr.title, 
                "user": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "mergeable": pr.mergeable
            } for pr in pulls])
        except Exception as e:
            logging.error(f"❌ Error fetching PRs: {e}")
            return jsonify({"error": str(e)}), 500