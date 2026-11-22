"""Public REST observation of the fixed, merged approval smoke test."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone

OWNER = "mashimashiman-max"
REPO = OWNER + "/haro-trust-governance"
REPO_ID = 1467202772
OWNER_ID = 359733728
AUTHOR = "mmibu1939-debug"
AUTHOR_ID = 264738043
RULE_ID = 27826104
HEAD = "1d1e2ad38b68b0de0c23c6562e788cb430ff4ba3"
MERGE = "9668041977090871bd75ba1f6e5012e43093918d"
BASE = "12da0ba304608e7a0a075190a080a500eeabf78a"
API = "https://api.github.com/repos/" + REPO
UNSIGNED = "GH_API_REVIEW_VERIFIED_NOT_CRYPTO_SIGNED"


class Rejected(ValueError):
    pass


def need(condition, reason):
    if not condition:
        raise Rejected(reason)


def parse_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, "duplicate_json_key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: need(False, "invalid_json_number"))


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def gh(*args):
    env = dict(os.environ, GH_PROMPT_DISABLED="1", GH_NO_UPDATE_NOTIFIER="1")
    env.pop("GH_DEBUG", None)
    res = subprocess.run(["gh", *args], capture_output=True, env=env, timeout=90)
    if res.returncode:
        status = re.search(rb"\bHTTP ([45][0-9]{2})\b", res.stderr)
        reason = "gh_http_" + status[1].decode() if status else "gh_request_failed"
        raise Rejected(reason + "_exit_" + str(res.returncode))
    return parse_json(res.stdout)


def api(path, paged=False):
    args = ["api", "--hostname", "github.com", "--method", "GET"]
    if paged:
        args.extend(["--paginate", "--slurp"])
    data = gh(*args, "repos/" + REPO + path)
    if not paged:
        return data
    need(type(data) is list and all(type(page) is list for page in data), "invalid_pages")
    return [item for page in data for item in page]


def instant(value):
    need(isinstance(value, str) and re.fullmatch(
        r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,9})?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)", value, re.ASCII)
        and not value.endswith("-00:00"), "invalid_timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def sha(value):
    need(isinstance(value, str) and re.fullmatch("[0-9a-f]{40}", value), "invalid_commit_sha")
    return value


def repo_identity(repo):
    need(repo["full_name"] == REPO and repo["id"] == REPO_ID and repo["private"] is False,
         "wrong_repository")


def user_identity(user, login, uid):
    need(user["type"] == "User" and user["login"] == login and user["id"] == uid,
         "wrong_github_identity")


def ruleset(data, submitted):
    need(data["id"] == RULE_ID and data["source"] == REPO and data["source_type"] == "Repository"
         and data["name"] == "haro-main-approval" and data["target"] == "branch"
         and data["enforcement"] == "active", "ruleset_identity_or_enforcement")
    need(data["conditions"] == {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
         "ruleset_scope")
    # GitHub omits bypass metadata for non-admin credentials. This is an
    # API observation, not formal governance qualification: retain unknown
    # rather than claiming bypass list empty or disabling signed provenance.
    bypass_visible = "bypass_actors" in data
    if bypass_visible:
        need(data["bypass_actors"] == [], "ruleset_has_bypass")
    matches = [rule["parameters"] for rule in data["rules"] if rule["type"] == "pull_request"]
    need(len(matches) == 1, "missing_pr_rule")
    params = matches[0]
    count = params["required_approving_review_count"]
    need(type(count) is int and count == 1 and params["require_last_push_approval"] is True
         and params["dismiss_stale_reviews_on_push"] is True, "ruleset_requirements")
    need(instant(data["created_at"]) <= instant(data["updated_at"]) <= submitted,
         "ruleset_revision_postdates_approval")
    return {"id": RULE_ID, "name": data["name"], "source": REPO, "enforcement": "active",
            "conditions": data["conditions"], "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "bypass_actors": [] if bypass_visible else None,
            "bypass_metadata_visible": bypass_visible,
            "full_governance_policy_verified": bypass_visible,
            "required_approving_review_count": count, "require_last_push_approval": True,
            "dismiss_stale_reviews_on_push": True}


def require_ancestor(get, ancestor, descendant):
    comparison = get("/compare/" + sha(ancestor) + "..." + sha(descendant))
    need(comparison["status"] == ("identical" if ancestor == descendant else "ahead")
         and comparison["behind_by"] == 0 and comparison["base_commit"]["sha"] == ancestor
         and comparison["merge_base_commit"]["sha"] == ancestor, "main_ancestry")


def collect(pr, main_at_collection=None, get=api, now=None):
    need(pr == "1", "only_public_smoke_pr_1")
    now = now or datetime.now(timezone.utc)
    repo = get("")
    repo_identity(repo)
    need(repo["visibility"] == "public" and repo["default_branch"] == "main", "repository_scope")
    user_identity(repo["owner"], OWNER, OWNER_ID)
    pull = get("/pulls/1")
    repo_identity(pull["base"]["repo"])
    repo_identity(pull["head"]["repo"])
    user_identity(pull["user"], AUTHOR, AUTHOR_ID)
    need(pull["id"] == 5435880926 and type(pull["number"]) is int and pull["number"] == 1
         and pull["state"] == "closed" and pull["merged"] is True, "pr_not_merged_or_wrong_id")
    need(pull["base"]["ref"] == "main" and pull["base"]["sha"] == BASE
         and pull["head"]["sha"] == HEAD and pull["merge_commit_sha"] == MERGE, "pr_revision")

    reviews = get("/pulls/1/reviews?per_page=100", True)
    approvals = []
    for review in reviews:
        need(review["pull_request_url"] == API + "/pulls/1", "review_scope")
        need(review["state"] in ("APPROVED", "COMMENTED"), "unresolved_or_dismissed_review")
        if review["state"] == "APPROVED":
            user_identity(review["user"], OWNER, OWNER_ID)
            need(review["author_association"] == "OWNER" and review["commit_id"] == HEAD,
                 "reviewer_or_head")
            approvals.append(review)
    need(len(approvals) == 1 and approvals[0]["id"] == 6010452286, "approval_identity")
    review = approvals[0]
    submitted = instant(review["submitted_at"])
    merged = instant(pull["merged_at"])
    need(instant(pull["created_at"]) <= submitted <= merged <= now
         and merged - submitted <= timedelta(days=1), "expired_or_unordered_review")

    commits = get("/pulls/1/commits?per_page=100", True)
    need(len(commits) == pull["commits"] == 1 and commits[0]["sha"] == HEAD, "commit_set")
    for role in ("author", "committer"):
        user_identity(commits[0][role], AUTHOR, AUTHOR_ID)
    merge = get("/commits/" + MERGE)
    tree = sha(commits[0]["commit"]["tree"]["sha"])
    need(merge["sha"] == MERGE and [p["sha"] for p in merge["parents"]] == [BASE]
         and merge["commit"]["tree"]["sha"] == tree, "squash_merge_binding")
    ref = get("/git/ref/heads/main")
    need(ref["ref"] == "refs/heads/main" and ref["object"]["type"] == "commit", "main_ref")
    current = sha(ref["object"]["sha"])
    anchor = current if main_at_collection is None else sha(main_at_collection)
    require_ancestor(get, MERGE, anchor)
    if current != anchor:
        require_ancestor(get, anchor, current)
    policy = ruleset(get("/rulesets/" + str(RULE_ID)), submitted)
    return {"type": "github.approval-observation.v1", "verdict": UNSIGNED, "formal": False,
            "repository": REPO, "repository_id": REPO_ID, "pr_number": 1, "pr_id": pull["id"],
            "created_at": pull["created_at"], "merged_at": pull["merged_at"], "base_ref": "main",
            "author": AUTHOR, "author_id": AUTHOR_ID, "head_sha": HEAD, "base_sha": BASE,
            "merge_sha": MERGE, "main_sha": anchor, "tree_sha": tree, "ruleset": policy,
            "review": {"id": review["id"], "reviewer": OWNER, "reviewer_id": OWNER_ID,
                       "state": "APPROVED", "commit_id": HEAD, "submitted_at": review["submitted_at"]}}


ROOT = Path(__file__).resolve().parents[1]


def write_atomic(name, data):
    need(name in ("approval-evidence.json", "supplemental-receipt.json"), "output_scope")
    path = ROOT / name
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as out:
        try:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        except BaseException:
            os.unlink(out.name)
            raise
    try:
        os.replace(out.name, path)
    finally:
        Path(out.name).unlink(missing_ok=True)


def guarded(function):
    try:
        function()
    except (OSError, ValueError, KeyError, IndexError, TypeError, OverflowError,
            subprocess.SubprocessError) as exc:
        # Neither API bodies, input JSON, credentials nor gh stderr are safe diagnostics.
        reason = str(exc) if type(exc) is Rejected else "invalid_or_unavailable_metadata"
        print(json.dumps({"status": "REJECTED", "reason": reason, "formal": False}), file=sys.stderr)
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", required=True)
    parser.add_argument("--main-sha")
    args = parser.parse_args()
    write_atomic("approval-evidence.json", encode(collect(args.pr, args.main_sha)))


if __name__ == "__main__":
    sys.exit(guarded(main))
