import sys
sys.path.append('src')
import mcmc_norm_learning
import yaml
import shutil

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
true_norm_name = params['true_norm']['name']
true_norm_exp = params['true_norm']['exp']
colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area = params['target_area']

print(f'True norm name: {true_norm_name}')
print(f'True norm exp: {true_norm_exp}')
print(f'Target area: {target_area}; {type(target_area)}')


#colour_specific: ['r', 'g', 'b']
#shape_specific: ['square', 'circle', 'triangle']
#target_area: -0.8, 0.7 ; 0.25, 0.99

if true_norm_name = 'default':
    shutil.copyfile('data/default_env.pickle', 'data/env.pickle')
else:
    print('To do: generate new env')
    

