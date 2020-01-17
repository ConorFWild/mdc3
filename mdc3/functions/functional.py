

def mapdict(func, dictionary, executor):
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    results = executor(func,
                       values,
                       )

    return {key: result for key, result in zip(keys, results)}



def wrap_call(x):
    return x()


