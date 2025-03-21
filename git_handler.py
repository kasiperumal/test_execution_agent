import git
import os
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def clone_or_update_repo():
    repo_path = "test_repo"
    if os.path.exists(repo_path):
        repo = git.Repo(repo_path)
        repo.remotes.origin.pull()
    else:
        git.Repo.clone_from(config["git_repo"], repo_path, branch=config["branch"])

if __name__ == "__main__":
    clone_or_update_repo()
