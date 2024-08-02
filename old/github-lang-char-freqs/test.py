import re
import subprocess

# m = re.search('(?<=abc)def', 'abcdef')
# print(re.compile('Isaac (?!Asimov)').findall('aIsaac x'))

diff = subprocess.Popen('git -C ~/.emacs.d diff HEAD~2 --unified=0 --word-diff', shell=True)
# subprocess.Popen(['git', '-C', '/home/xged/.emacs.d', 'diff', 'HEAD~2', '--unified=0', '--word-diff'])

langRegex = re.compile('(?<=\+\+\+ .+\.).+?(?=\n)').findall(diff)
print(langRegex)
