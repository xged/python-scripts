import subprocess
from collections import Counter
from copy import deepcopy as copy
from datetime import date, timedelta
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import regex
import requests
from icecream import ic

RepoCounter = tuple[Counter['Char'], {'RepoUrl'}]  # tuple=SimpleNamespace

def shell(s:str): return subprocess.run(s, capture_output=True, check=True, shell=True, text=True).stdout

def getRepos(params={'q':'stars:>0'}, n=1000)->{'RepoUrl'}:  #!? stars:>=0 # noqa
    assert n<=1000
    perPage = min(100, n)
    npages = n//100 or 1
    urls = set()
    for page in range(1, npages+1):
        rjson = requests.get('https://api.github.com/search/repositories', {'per_page':perPage, 'page':page, **params}).json()
        for repoItem in rjson['items']: urls.add(repoItem['clone_url'])
    return urls

def doCommits(repoUrls, inLast_years=5.0, commitCharMax=5000,
              rc:RepoCounter=SimpleNamespace(counter=Counter(), repoUrls=set()))->RepoCounter:
    rc = copy(rc)
    since = date.today()-timedelta(365*inLast_years)
    repoUrls = set(repoUrls)-rc.repoUrls
    for repoUrl in repoUrls:
        print(repoUrl, ': processing..')
        rc.repoUrls.add(repoUrl)
        with TemporaryDirectory() as fp:
            shell(f"git clone {repoUrl} {fp} --shallow-since={since} --shallow-submodules")
            commitHashes = shell(f"git -C {fp} log --pretty=format:%H").split()[:-1]
            assert len(commitHashes)!=0
            for commitHash in commitHashes:
                try:
                    diffPatch = shell(f"git -C {fp} diff {commitHash}~ {commitHash} --word-diff=porcelain --word-diff-regex=. --unified=0")
                    for diff in diffPatch.split("diff --git a/")[1:]:
                        if len(diff)<=commitCharMax:
                            addedLines = regex.findall(r"\n\+(?!\+\+ [ab/])(.+)", diff)
                            rc.counter += Counter(''.join(addedLines))
                except Exception as er: print(er)
    for c in set(rc.counter.keys()):
        if c in (')',']','}','\n','\r','\t') or not c.isascii(): del rc.counter[c]
    return rc

def main(params={'q':'stars:>0'}, n=1000, inLast_years=5, commitCharMax=5000,
         rc:RepoCounter=SimpleNamespace(counter=Counter(), repoUrls=set()))->RepoCounter:
    return doCommits(getRepos(params, n), inLast_years, commitCharMax, rc)
