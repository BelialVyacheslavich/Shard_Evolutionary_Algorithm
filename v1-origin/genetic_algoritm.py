import numpy as np
import random
import math


isMaximisation = False
func_type = "r"


def calc_function(arr):
    x = arr[0]
    y = arr[1]
    val = None
    if func_type == "p":
        val = (x - 1) ** 2 + (y - 1) ** 2
    elif func_type == "r":
        val = 0
        A = 10
        for x in arr:
            val += (x ** 2) - A * math.cos(2 * math.pi * x)
        val += A * arr.shape[0]
    return val


class Individual:
    def __init__(self, variables):
        self.variables = variables  # x,y,z,..
        self.value = calc_function(variables)
        self.is_made_children = False
        self.child_count = None
        self.life_time = None
        self.radius = 0.25

    def tick(self):
        # True if Alive
        self.life_time -= 1
        if self.life_time <= 0:
            return False
        else:
            return True

    def made_children(self):
        self.is_made_children = True
        return self.child_count

    def __repr__(self):
        return "<Ind: value=%r ; vars=%r>" % (self.value, self.variables)


def value_key(x):
    return x.value


class Population:
    def __init__(self, init_count, max_population, var_count, var_borders, calc_count=5000):
        self.individuals = list()
        self.var_count = var_count
        self.var_borders = var_borders
        self.max_population = max_population
        self.max_calculation_count = calc_count
        self.calc_count = init_count
        for x in range(init_count):
            ar = np.zeros(shape=(var_count))
            for v in range(var_count):
                r = random.uniform(var_borders[v][0], var_borders[v][1])
                ar[v] = r
            self.individuals.append(Individual(ar))
        self.cache_list = list()
        self.cache_max = 1
        self.gen_history = list()
        self.evolve()

    def sort_by_value(self, subpop):
        subpop = sorted(subpop, key=value_key)
        global isMaximisation
        if isMaximisation:
            subpop.reverse()
        return subpop

    def evolve(self):
        # Mutation - None
        # Crossover - Child Dotes?
        # Selection - Extinction
        while not self.check_stop():
            self.perform_generation_step()

    def check_stop(self):
        if self.calc_count < self.max_calculation_count:
            return False
        else:
            return True

    def make_children(self, ind):
        children = list()
        for x in range(ind.child_count):
            ar = np.zeros(shape=(self.var_count))
            for v in range(self.var_count):
                xvar = ind.variables[v]
                rad = ind.radius
                var = random.uniform(xvar - rad, xvar + rad)
                # border check
                while var < self.var_borders[v][0] or var > self.var_borders[v][1]:
                    var = (var + xvar) / 2
                ar[v] = var
            children.append(Individual(ar))
        return children

    def compare_individuals(self, ind1, ind2):
        # 0 if ind1 = ind2
        # 10 if ind1.value = ind2.value, but vars not
        # -1 if ind1.value better than ind2.value
        # 1 if ind2.value better than ind1.value

        if isMaximisation:
            if ind1.value > ind2.value:
                return -1
            elif ind2.value > ind1.value:
                return 1
            else:
                is_same = True
                for x in range(self.var_count):
                    if ind1.variables[x] is not ind2.variables[x]:
                        is_same = False
                        break
                if is_same:
                    return 0
                else:
                    return 10
        else:
            if ind1.value < ind2.value:
                return -1
            elif ind2.value < ind1.value:
                return 1
            else:
                is_same = True
                for x in range(self.var_count):
                    if ind1.variables[x] != ind2.variables[x]:
                        is_same = False
                        break
                if is_same:
                    return 0
                else:
                    return 10

    def cache_individual(self, individual):
        last = self.cache_list.__len__()
        if last is 0:
            self.cache_list.append(individual)
            return None
        else:
            self.cache_list = self.sort_by_value(self.cache_list)
            comparelist = list()
            for x in self.cache_list:
                compare = self.compare_individuals(individual, x)
                if compare is 0:
                    # if individual already cached
                    return None
                comparelist.append(compare)
            if last < self.cache_max:
                self.cache_list.append(individual)
            else:
                last_worst = None
                for x in range(self.cache_max):
                    if comparelist[x] is -1:
                        last_worst = x
                        break
                if last_worst is None:
                    return None
                else:
                    new_cache = list()
                    for x in range(self.cache_max):
                        if x < last_worst:
                            new_cache.append(self.cache_list[x])
                        elif x is last_worst:
                            new_cache.append(individual)
                        else:
                            new_cache.append(self.cache_list[x - 1])
                    self.cache_list = new_cache

    def perform_generation_step(self):
        # Evaluation
        # Spreading
        # Extinction and Saving the bests
        # ________________________________
        # Step 1: evaluate all individuals
        # give them corresponding child count
        # and life time
        # -----------------------------------

        subpop = list()
        for x in self.individuals:
            if not x.is_made_children:
                subpop.append(x)
        subpop = self.sort_by_value(subpop)
        count = subpop.__len__()
        b_top = math.ceil(count / 3)
        b_mid = 2 * b_top
        # print("count: " + count.__str__())
        for x in range(count):
            if x < b_top:
                subpop[x].child_count = 3
                subpop[x].life_time = 3
                # print(x.__str__() + " top")
            elif x < b_mid:
                subpop[x].child_count = 2
                subpop[x].life_time = 2
                # print(x.__str__() + " mid")
            else:
                subpop[x].child_count = 1
                subpop[x].life_time = 1
                # print(x.__str__() + " bot")

        # -----------------------------------
        # Step 2: spreads children
        # in radius from parent
        # -----------------------------------

        newpop = list()
        children = list()
        for x in subpop:
            x.is_made_children = True
            ch = self.make_children(x)
            self.calc_count += ch.__len__()
            children.extend(ch)

        newpop.extend(subpop)
        for x in self.individuals:
            if x.is_made_children:
                newpop.append(x)
        self.individuals = newpop

        # -----------------------------------
        # Step 3: sort individuals by value
        # let die, if life time is end
        # kill weak individuals
        # if population is too big
        # -----------------------------------

        newpop = list()
        for x in self.individuals:
            alive = x.tick()
            if alive:
                newpop.append(x)

        # Collect to cache

        for x in self.individuals:
            self.cache_individual(x)
        for x in children:
            self.cache_individual(x)

        # Collect all together and kill
        newpop.extend(children)
        newpop = self.sort_by_value(newpop)
        pop = list()
        for x in range(self.max_population):
            try:
                pop.append(newpop[x])
            except:
                # Sometimes, population is smaller than maximum population count
                pass

        self.individuals = pop
        # Save each generation for plots
        self.gen_history.append(self.individuals)


def return_population(init_count, max_count, var_count, borders):
    pop = Population(init_count, max_count, var_count, borders)
    return pop
