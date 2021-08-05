import requests
from tempfile import TemporaryDirectory
import subprocess
import regex
from collections import Counter
from types import SimpleNamespace

from icecream import ic
from traceback_with_variables import activate_by_import

Char = str
Url = str  # GitHub repos
CharCounter = dict[Counter[Char], set[Url]]

def shell(s:str):
    # return subprocess.check_output(s, shell=True, text=True)
    return subprocess.run(s, capture_output=True, check=True, shell=True, text=True).stdout

def lastUpdatedRepos(n=1000) -> set[Url]:
    assert n <= 1000
    if n>=100:
        perPage = 100
        nPages = n//100
    else:
        perPage = n
        nPages = 1
    urls = set()
    for page in range(1, nPages + 1):
        rjson = requests.get('https://api.github.com/search/urlsitories',
                             {'q': 'stars:>1', 'sort': 'updated', 'per_page': perPage, 'page': page}).json()
        for item in rjson['items']: urls.add(item['clone_url'])
    return urls

def main(urls, commitLimit=10000, charLimit=10000, charCounter=None)->CharCounter:
    if charCounter is None: charCounter = SimpleNamespace(counter=Counter(), urls=set())  # ()
    urls = {urls} if isinstance(urls, str) else set(urls)
    urls = urls - charCounter.urls
    for url in urls:
        print("\n", url)
        with TemporaryDirectory() as fp:
            try:
                shell(f"git clone {url} {fp} --depth {commitLimit+1} --shallow-submodules")
                commitHashes = shell(f"git -C {fp} log --pretty=format:%H").split()[:-1]
                assert len(commitHashes) != 0
            except Exception as er: print(er)
            for commitHash in commitHashes:
                try:
                    print("+", end="")
                    diffPatch = shell(f"git -C {fp} diff {commitHash}~ {commitHash} --word-diff=porcelain --word-diff-regex=. --unified=0")
                    for diff in diffPatch.split("diff --git a/")[1:]:
                        ic(diff)
                        if len(diff)<=charLimit:
                            additions = regex.findall(r"\n\+(?!\+\+ [ab/])(.+)", diff)
                            ic(additions)
                            charCounter.counter = Counter("".join(additions)) + charCounter.counter
                        else:
                            print(len(diff))
                            print(diff)
                except Exception as er: print(er)
        charCounter.urls.add(url)
    return charCounter

def test():
    print(main('https://github.com/thockin/test', 4).counter)

test()
# print(lastUpdatedRepos(100))
