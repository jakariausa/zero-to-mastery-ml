import requests
import base64
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
if not dotenv_path:
    print(".env file not found. Ensure environment variables are set.")
else:
    load_dotenv(dotenv_path)

token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}
print(headers)
# GitHub repository info
owner = "jakariausa"
repo = "zero-to-mastery-ml"
path = "section-2-data-science-and-ml-tools/car-sales-data-manufacture.ipynb"  # Relative path to the file

# GitHub API URL
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
print("URL", url)
response = requests.get(url, headers=headers)
if response.status_code == 200:
    content = response.json()["content"]
    code = base64.b64decode(content).decode("utf-8")
    print(code)  # This is your file content as a string
else:
    print("Failed to fetch file:", response.status_code)
