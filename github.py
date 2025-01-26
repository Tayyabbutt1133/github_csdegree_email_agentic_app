import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github_repos(owner):
    url = f"https://api.github.com/users/{owner}/repos"
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Data not found with Status code:", response.status_code)
        data = []
    
    return data


def get_github_data(owner):
    data = fetch_github_repos(owner)
    return load_github_repos(data)



def load_github_repos(data):
    docs = []
    for entry in data:
        metadata = {
            "name": entry["name"],
            "description": entry["description"],
            "html_url": entry["html_url"],
            "created_at": entry["created_at"],
            "updated_at": entry["updated_at"],
            "language": entry["language"],
            "stargazers_count": entry["stargazers_count"],
            "forks_count": entry["forks_count"],
            "open_issues_count": entry["open_issues_count"],
            "default_branch": entry["default_branch"],
        }
          # Create a string summarizing the repository data
        page_content = f"Repository Name: {entry['name']}\nDescription: {entry['description'] or 'No description available.'}"
        
        doc = Document(page_content=page_content, metadata= metadata)
        docs.append(doc)
    return docs



    
# github_response = fetch_github_repos("Tayyabbutt1133")

# repo_name = load_github_repos(github_response)
# # Print the complete repository metadata
# print("Repository Metadata:")
# for repo in repo_name:
#     print(repo)