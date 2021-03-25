import subprocess
from collections import Counter
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import regex
import requests
from icecream import ic
# from traceback_with_variables import activate_by_import

Char = str
Url = str  # GitHub repos
RepoCounter = dict[Counter[Char], set[Url]]  # dict=SimpleNamespace

def shell(s:str): return subprocess.run(s, capture_output=True, check=True, shell=True, text=True).stdout

def main(params:dict=None, n=1000, commitLimit=10000, charLimit=10000, repoCounter=None):
    if params is None: params = {'q':'stars:>=0'}
    if repoCounter is None: repoCounter = SimpleNamespace(counter=Counter(), repos=set())
    assert n <= 1000

    def doCommits(repo:Url):
        counter = Counter()
        with TemporaryDirectory() as fp:
            shell(f"git clone {repo} {fp} --depth {commitLimit+1} --shallow-submodules")
            commitHashes = shell(f"git -C {fp} log --pretty=format:%H").split()[:-1]
            assert len(commitHashes) != 0
            for commitHash in commitHashes:
                try:
                    print("+", end="")
                    diffPatch = shell(f"git -C {fp} diff {commitHash}~ {commitHash} --word-diff=porcelain --word-diff-regex=. --unified=0")
                    for diff in diffPatch.split("diff --git a/")[1:]:
                        if len(diff)<=charLimit:
                            addedLines = regex.findall(r"\n\+(?!\+\+ [ab/])(.+)", diff)
                            counter += Counter(''.join(addedLines))
                        else:
                            print(len(diff))
                            print(diff)
                except Exception as er: print(er)
        for c in list(repoCounter.counter.keys()):
            if c in (')',']','}','\n','\r') or not c.isascii(): del repoCounter.counter[c]
        repoCounter.counter += counter
        repoCounter.repos.add(repo)

    if n>=100:
        perPage = 100
        npages = n//100
    else:
        perPage = n
        npages = 1
    for page in range(1, npages+1):
        rjson = requests.get('https://api.github.com/search/repositories', {'per_page':perPage,'page':page,**params}).json()
        for item in rjson['items']:
            repo = item['clone_url']
            if repo not in repoCounter.repos:
                print("\n", repo)
                doCommits(repo)
    return repoCounter
