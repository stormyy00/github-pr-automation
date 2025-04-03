from flask import Flask, request, jsonify
from app.config import repo
from ..utils.analyze import analyze_pr
from ..utils.automerge import auto_merge_pr

class Merge:
    @staticmethod
    def merge_pr(pr_number):
        try:
            review = analyze_pr(pr_number)
            success, message = auto_merge_pr(pr_number, review)

            return jsonify({
                "pr_number": pr_number,
                "success": success,
                "message": message,
                "review": review
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500