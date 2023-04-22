import re


class GithubHash:
    def __init__(self, hash_str):
        if re.match(r"[a-f0-9]{40}", hash_str):
            self.hash = hash_str
        else:
            raise Exception("Invalid hash")

    def __str__(self):
        return self.hash

    def __repr__(self):
        return f"GithubHash('{self.hash}')"
