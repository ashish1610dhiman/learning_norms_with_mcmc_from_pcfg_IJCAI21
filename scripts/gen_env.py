import sys
sys.path.append('src')

import yaml
import shutil

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
env_name = params['env_name']
if env_name == 'default':
    shutil.copyfile('data/default_env.pickle', 'data/env.pickle')
else:
    assert 'Generating new environment is not currently supported' and False



