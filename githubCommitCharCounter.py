import subprocess
from collections import Counter
from datetime import date, timedelta
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import regex
import requests
from icecream import ic

Char = str
Url = str  # GitHub repos
RepoCounter = dict[Counter[Char], {Url}]  # dict=SimpleNamespace

def shell(s:str): return subprocess.run(s, capture_output=True, check=True, shell=True, text=True).stdout

def getRepos(params:dict=None, n=1000)->{Url}:
    if params is None: params = {'q':'stars:>0'}  # !? stars:>=0
    assert n <= 1000
    perPage = min(100, n)
    npages = n//100 or 1
    urls = set()
    for page in range(1, npages+1):
        rjson = requests.get('https://api.github.com/search/repositories', {'per_page':perPage,'page':page,**params}).json()
        for repoItem in rjson['items']:
            urls.add(repoItem['clone_url'])
    return urls

def doCommits(repos:{Url}, inLastYears=5, commitCharMax=5000, rc:RepoCounter=None)->RepoCounter:
    if rc is None: rc = SimpleNamespace(counter=Counter(), repos=set())
    since = date.today()-timedelta(365*inLastYears)
    repos = set(repos)-rc.repos
    for repo in repos:
        print(repo, ': processing..')
        rc.repos.add(repo)
        with TemporaryDirectory() as fp:
            shell(f"git clone {repo} {fp} --shallow-since={since} --shallow-submodules")
            commitHashes = shell(f"git -C {fp} log --pretty=format:%H").split()[:-1]
            assert len(commitHashes) != 0
            for commitHash in commitHashes:
                try:
                    diffPatch = shell(f"git -C {fp} diff {commitHash}~ {commitHash} --word-diff=porcelain --word-diff-regex=. --unified=0")
                    for diff in diffPatch.split("diff --git a/")[1:]:
                        if len(diff)<=commitCharMax:
                            addedLines = regex.findall(r"\n\+(?!\+\+ [ab/])(.+)", diff)
                            rc.counter += Counter(''.join(addedLines))
                except Exception as er: print(er)
    for c in list(rc.counter.keys()):
        if c in (')',']','}','\n','\r') or not c.isascii(): del rc.counter[c]
    return rc

def main(params:dict=None, n=1000, inLastYears=5, commitCharMax=5000, rc:RepoCounter=None)->RepoCounter:
    return doCommits(getRepos(params, n), inLastYears, commitCharMax, rc)
