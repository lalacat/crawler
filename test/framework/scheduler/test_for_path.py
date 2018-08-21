import os
from test.framework.setting import Setting

s = Setting()
def job_dir(settings):
    #path = settings['JOBDIR']
    path = settings['JOBDIR']
    if path and not os.path.exists(path):
        os.makedirs(path)
    return path

p = job_dir(s)
if p :
    print(p)
