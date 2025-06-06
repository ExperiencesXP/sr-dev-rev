import os
import cohere
from cohere.errors import CohereError
from github import Github

def estimate_tokens(text: str) -> int:
    # Rough heuristic: 1 token ≈ 4 characters
    return int(len(text) / 4)

# Read secrets from environment variables

cohere_api_key = os.environ.get("COHERE_API_KEY", "").strip()
gh_token = os.environ.get("TOKEN_GITHUB", "").strip()

if not cohere_api_key:
    raise RuntimeError("Missing or empty COHERE_API_KEY environment variable")

if not gh_token:
    raise RuntimeError("Missing or empty TOKEN_GITHUB environment variable")

# GitHub setup
repo_name = os.environ.get("GITHUB_REPOSITORY")
if not repo_name:
    raise RuntimeError("GITHUB_REPOSITORY environment variable not set.")
g = Github(gh_token)
repo = g.get_repo(repo_name)
latest_commit = repo.get_commits()[0]
commit_message = latest_commit.commit.message.strip()

# Load prompt template
with open("prompt.txt", "r", encoding="utf-8") as f:
    template = f.read()

# Cohere client
client = cohere.Client(cohere_api_key)

# Skip conditions
MAX_PATCH_LENGTH = 3000          # character-based safety
MAX_TOKENS_PER_FILE = 10000      # token-based safety
skip_log = []
comments = []

for file in latest_commit.files:
    if file.filename.startswith("venv/"):
        continue

    patch = getattr(file, "patch", None)
    if not patch:
        continue

    if len(patch) > MAX_PATCH_LENGTH:
        skip_log.append(f"Skipped `{file.filename}` due to size ({len(patch)} characters).")
        continue

    token_estimate = estimate_tokens(patch)
    if token_estimate > MAX_TOKENS_PER_FILE:
        skip_log.append(f"Skipped `{file.filename}` due to token estimate ({token_estimate} tokens).")
        continue

    prompt = (
        template.replace("{{DIFF}}", patch)
                .replace("{{MESSAGE}}", commit_message)
    )

    # Try command-a, fallback chain
    try:
        response = client.chat(
            message=prompt,
            model="command-r-plus",
            temperature=0.6,
        )
    except CohereError as e1:
        print(f"command-r-plus failed: {e1}. Falling back to command-r...")
        response = client.chat(
            message=prompt,
            model="command-r",
            temperature=0.6,
        )

    review = response.text.strip()
    if review:
        comments.append(f"**File: `{file.filename}`**\n\n{review}")

# Post to GitHub
issues = repo.get_issues(state='open')
issue = issues[0] if issues.totalCount > 0 else repo.create_issue(title="Code Review Comments")

if comments:
    issue.create_comment("\n\n---\n\n".join(comments))
if skip_log:
    issue.create_comment("**Skipped Files:**\n\n" + "\n".join(skip_log))

print("Review posted using Cohere.")
