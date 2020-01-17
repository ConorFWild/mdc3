from typing import Dict


class HashMap:
    def __init__(self, dictionary: Dict):
        self._dictionary = dictionary

    def __getitem__(self, item):
        return self._dictionary[item]

    def __setitem__(self, key, value):
        self._dictionary[key] = value

    def bind(self, func, executor=map):
        keys = [key for key in self._dictionary.keys()]
        values = [value for value in self._dictionary.values()]

        results = executor(func,
                           values,
                           )

        new_dict = {key: result for key, result in zip(keys, results)}

        return HashMap(new_dict)
