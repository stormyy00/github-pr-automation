from flask import jsonify

import logging
import requests
import json
from github import Github
from flask import Flask, request, jsonify
from app.utils.analyze import analyze_pr

class Review:
     @staticmethod
     def review_pr(pr_number):
        try:
            review = analyze_pr(pr_number)
            return jsonify({"pr_number": pr_number, "review": review})
        except Exception as e:
            logging.error(f"❌ Error analyzing PR #{pr_number}: {e}")
            return jsonify({"error": str(e)}), 500

