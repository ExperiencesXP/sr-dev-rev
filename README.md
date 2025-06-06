# sr-dev-rev
## Senior Developer (Code) Review

**This project sets up an AI-powered** ***senior*** **developer that reviews your commits like it's the 1000th time you've made that mistake.**

---

## How It Works
Every time you push to the `main` branch (or however you configure it), a GitHub Action runs a Python script that:

1. Fetches your latest commit.
2. Sends the code to OpenAI’s API with a prompt designed to simulate a very tired, very passive-aggressive senior developer.
3. Posts the resulting roast directly as a comment on your repo.

---

## Features

- **Triggered on push** – No PR required.
- **Roasts included** – Snark, sarcasm, and actual education.
- **Action-based** – Fully integrated into GitHub Actions.
- **Fix suggestions** – Not just insults—solutions too.
- **Tips and best practices** – Learn from the pain.

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/ExperiencesXP/sr-dev-rev
cd sr-dev-rev
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install cohere pygithub
```

### 4. Generate the secrets

**Cohere API Keey:** Create a free account at [cohere.com](https://dashboard.cohere.com/api-keys), then generate your API key from the dashboard.
**GitHub Personal Access Token:** Go to [GitHub Tokens Settings](https://github.com/settings/tokens), and generate a token with the `repo` scope enabled to allow access to your repositories.

## Either use a `.env` file as instructed in step 4. or add your secrets to your repo as instructed in step 5.

### 5. Add .env File

```bash
COHERE_API_KEY="Your Cohere API Key"
TOKEN_GITHUB="Your Github Token"
```

### 6. Set Up GitHub Secrets

In your GitHub repo settings, go to:
`Settings → Secrets and variables → Actions → New repository secret`

Add:

- COHERE_API_KEY
- TOKEN_GITHUB

### 7. Confirm the reviewer works

Push changes to a repository with sr-dev-rev in it. An issue should open where future comments should be posted.
You can also confirm by going into your actions and verifying if the workflow is running.

## License

This project is licensed under a [Custom Non-Commercial License](./LICENSE.txt).  
You may use, modify, and share the code **non-commercially**, with **attribution**.  
For commercial use, [contact me](mailto:gitexperiences@gmail.com).
