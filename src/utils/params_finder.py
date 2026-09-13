from abc import ABC, abstractmethod
from functools import partial
from itertools import product
from multiprocessing import Pool

import numpy as np


class ParamsFinder(ABC):
    def __init__(self):
        self.__param_ranges = None
        self.__max_seed = 100_000

    def with_parameter_space(self, param_ranges):
        self.__param_ranges = param_ranges
        return self

    def with_max_seed_attempts(self, max_seed):
        self.__max_seed = max_seed
        return self

    @abstractmethod
    def generator_factory():
        pass

    @abstractmethod
    def success_condition(self, params):
        pass

    @abstractmethod
    def space_check(self, params):
        pass

    def _try_seed_for_combination(self, params):
        next_gen = self.generator_factory(params)

        for seed in range(self.__max_seed):
            rng = np.random.default_rng(seed)

            if self.success_condition(next_gen(rng)):
                return params, seed

        return None

    def find_parallel(self):
        feasible_params = [
            params
            for params in product(*self.__param_ranges)
            if self.space_check(params)
        ]

        print(f"Допустимых комбинаций параметров: {len(feasible_params)}")

        if not feasible_params:
            return None

        search_func = partial(self._try_seed_for_combination)

        with Pool() as pool:
            for result in pool.imap_unordered(search_func, feasible_params):                
                if result is not None:
                    return result

        return None

    def find(self):
        feasible_params = [
            params
            for params in product(*self.__param_ranges)
            if self.space_check(params)
        ]

        print(f"Допустимых комбинаций: {len(feasible_params)}")
        if not feasible_params:
            return None

        for params in feasible_params:
            result = self._try_seed_for_combination(params)
            if result is not None:
                return result

        return None
