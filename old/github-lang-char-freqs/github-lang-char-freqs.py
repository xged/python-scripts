# TODO strings -> bytes
# TODO re -> splits

import pickle
import regex
import subprocess
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
# from typing import dict, list, Set, tuple
from warnings import warn
import os
import math
from contextlib import suppress

import requests
from whatthepatch import parse_patch

Char = str
RepoUrl = str
Freq = tuple[dict[Char, int], list[RepoUrl]]

# def charCounter(s):  # Case insensitive. Count uppercases as 2 (reason: avy-goto-word)
#     s = [char for char in s if char.isascii()]
#     s += [char.lower() for char in s if char.isupper()]
#     return Counter(s.lower())

# def make_LangFreqs(s, lang, langFreqs=None):
#     if langFreqs is None: langFreqs = {}
#     langFreqs[lang] = langFreqs.get(lang, Counter()) + charCounter(s)

def shell(s: str):
    # return subprocess.check_output(s, shell=True, text=True)
    return subprocess.run(s, capture_output=True, check=True, shell=True, text=True).stdout

# def shell(s): return subprocess.run(s.split(), capture_output=True, check=True, text=True).stdout

def main(repos, freq=None, commitLimit=1000, charLimit=10000) -> dict:
    # freq = {"freq": {}, "repos": set()} if freq is None else freq
    if freq is None: freq = {"freq": {}, "repos": set()}
    repos = {repos} if isinstance(repos, str) else set(repos)
    repos = repos - freq["repos"]
    langRegex = r"^\S+ b/\S+\w\.(\w+?)\n"
    additionsRegex = r"\n\+(?!\+\+ [ab/])(.+)"
    for repo in repos:
        print("\n", repo)
        with TemporaryDirectory() as fp:
            try:
                shell(f"git clone {repo} {fp} --depth {commitLimit} --shallow-submodules")
                commitHashes = shell(f"git -C {fp} log --pretty=format:%H").split()[:-1]
                assert len(commitHashes) != 0
            except Exception as er: print(er); continue
            for commitHash in commitHashes:
                try:
                    print("+", end="")
                    diffPatch = shell(f"git -C {fp} diff {commitHash}~ {commitHash} --word-diff=porcelain --word-diff-regex=. --unified=0")
                    for diff in diffPatch.split("diff --git a/")[1:]:
                        if len(diff) > charLimit:
                            print(len(diff))
                            print(diff)
                            continue
                        lang = regex.findall(langRegex, diff)
                        lang = lang[0] if lang else "None"
                        additions = regex.findall(additionsRegex, diff)
                        freq["freq"][lang] = Counter("".join(additions)) + freq["freq"].get(lang, Counter())
                except Exception as er: print(er); continue
        freq["repos"].add(repo)
    return freq

def lastUpdatedRepos(n=1000) -> Set[RepoUrl]:
    assert n <= 1000
    pages = (n + 99) // 100
    perPage = 100 if n > 100 else n
    repos = set()
    for page in range(1, pages + 1):
        r = requests.get('https://api.github.com/search/repositories',
                         {'q': 'stars:>1', 'sort': 'updated', 'page': page, 'per_page': perPage})
        for item in r.json()['items']:
            repos.add(item['clone_url'])
    return repos

repos = ['https://github.com/veron2/rainbow.git', 'https://github.com/CodeAcademyP307/05092018thirdlesson-mehebbethuseynov.git', 'https://github.com/Shadowz3n/CrowPSD.git', 'https://github.com/marcelocaldas/First_Project.git', 'https://github.com/NealO96/NealO96.github.io.git', 'https://github.com/y4d/flyingon-ui.git', 'https://github.com/marcuslavender/MyReactWebsite.git', 'https://github.com/devesh1296/Automatic-Checker-System-using-Facial-Rcognition-.git']

# main(lastUpdatedRepos(10))
# main("https://github.com/latinos/LatinoAnalysis.git")

def score(x):
    if x == 1: return 1
    return math.log(x, 1.5)

for x in range(1, 26):
    print(x, round(score(x)), round(score(x), 1))
for x in range(5, 10):
    x = 2**x
    print(x, round(score(x)), round(score(x), 1))
print(round(score(50)))

# fp = "/home/xged/src/config"
# commitHashes = shell(f"git -C {fp} log --pretty=format:%H").split()[:-1]
# for commitHash in commitHashes:
#     print(shell(f"git -C {fp} diff {commitHash}~ {commitHash} --word-diff=porcelain --word-diff-re=."))
# git -C /home/xged/src/config diff 90b3da095d09f838a90c325ba82afc249cf335b0~ 90b3da095d09f838a90c325ba82afc249cf335b0 --word-diff=porcelain --word-diff-re=.
