from src.utils.params_finder import ParamsFinder


class PFMean(ParamsFinder):
    def generator_factory(self, params):
        return lambda x: x.integers(*params).mean()

    def success_condition(self, candidate):
        return abs(candidate - 621) < 1e-9

    def space_check(self, params):
        low, high, size = params
        return low <= 621 <= (high - 1)


class PFStats(ParamsFinder):
    def generator_factory(self, params):
        return lambda x: x.integers(*params)

    def success_condition(self, candidate):
        return (
            candidate.min() == 621
            and candidate.max() == 621
            and candidate.mean() == 621
        )

    def space_check(self, params):
        low, high, size = params
        return low <= 621 <= (high - 1)


class PFMin(ParamsFinder):
    def generator_factory(self, params):
        return lambda x: x.integers(*params).min()

    def success_condition(self, candidate):
        return candidate == 621

    def space_check(self, params):
        low, high, size = params
        return low <= 621 <= (high - 1)


if __name__ == "__main__":
    # pf = PFMean().with_parameter_space([range(610, 615), range(630, 631), range(11, 20)])
    # pf = PFMin().with_parameter_space([range(500, 550), range(1700, 1800), range(10, 20)])
    pf = PFStats().with_parameter_space([range(518, 550), range(630, 650), range(3, 4)])

    result = pf.find_parallel()

    if result:
        params, seed = result

        print("Найдено!")
        print(f"Seed: {seed}")
        print(f"Параметры: {params}")

    else:
        print("Не найдено.")
