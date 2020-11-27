from typing import List
from packages.geneticAlgo.GeneticAlgorithm import GeneticAlgorithm
from packages.geneticAlgo.utils import roulette_wheel

from .Point import Point
from .PathItem import PathItem
from .utils import half, rand, push_to_list


class BestPathAlgorithm(GeneticAlgorithm[PathItem]):
    def __init__(self, mutation_chance: float, population_size: int, start: Point, end: Point):
        super().__init__(mutation_chance, population_size)
        self.start = start
        self.end = end

    def initial_population(self) -> List[PathItem]:
        return [
            PathItem.generate_path(self.start, self.end)
            for i in range(self.population_size)
        ]

    def should_stop(self) -> bool:
        pass

    def mating(self, parent1: PathItem, parent2: PathItem) -> PathItem:
        path: List[Point] = half(parent1.value) + half(parent2.value)

        return PathItem(path)

    def mutation(self, item: PathItem) -> PathItem:
        mutation_size = min(1, int(0.05 * self.population_size), len(item.value) // 2)
        start_index = rand(0, len(item.value) - 1 - mutation_size)

        for i in range(mutation_size):
            item.value.pop(start_index+i)

        return item

    def select_parents(self) -> (PathItem, PathItem):
        return roulette_wheel(self.population)

    def handle_erroneous(self, item: PathItem) -> PathItem:
        invalid_jump_index = item.invalid_jump_index()

        while invalid_jump_index != -1:
            start = item.value[invalid_jump_index-1]
            end = item.value[invalid_jump_index]
            fixed_path = PathItem.generate_path(start, end)

            item.value = push_to_list(item.value, invalid_jump_index-1, invalid_jump_index, fixed_path)

            invalid_jump_index = item.invalid_jump_index()

        return item

    def is_valid(self, item: PathItem) -> bool:
        return item.invalid_jump_index() != -1

