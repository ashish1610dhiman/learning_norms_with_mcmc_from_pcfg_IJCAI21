import sys
sys.path.append('src')

import pickle
from pickle_wrapper import unpickle, pickle_it

observations = unpickle('data/observations.pickle')
print(f'Length of observations is {len(observations)}')