import pickle

def unpickle(path):
    with open(path, 'rb') as fp:
        result = pickle.load(fp)
        # print("Unpickled 1st element for '{}' is {}\n".format(path, result[0]))
        return result

def pickle_it(x, path):
    with open(path, 'wb') as fp:
        pickle.dump(x, fp)