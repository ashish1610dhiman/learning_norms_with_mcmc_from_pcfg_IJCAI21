import sys
sys.path.append('src')
import mcmc_norm_learning
import yaml

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
true_norm_name = params['true_norm']['name']
true_norm_exp = params['true_norm']['exp']

print(f'True norm name: {true_norm_name}')
print(f'True norm exp: {true_norm_exp}')
print(type(true_norm_exp))
print(true_norm_exp[1][0])

# if true_norm_name = 'default':
    

