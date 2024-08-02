# from traceback_with_variables import activate_by_import
# print(gccc.main(params={'q':'stars:>0','sort':'updated'}, n=1, since='2021-02-02').counter)
from datetime import date
from pprint import pprint

import githubCommitCharCounter as gccc
import timetracker as tt

# print(gccc.main({'q':'stars:>0', 'sort':'updated'},1,1))
# print(getRepos(n=1))
# rjson=requests.get('https://api.github.com/repos/syl20bnr/spacemacs/issues', {'per_page':10,'since':2021}).json()
# print((rjson))

tt.addMinutes(2, 115)
tt.addMinutes(190)
print(tt.read())
tt.weekAvgs()
