import random, math, time

def distanceBetween(point1, point2):
    x_distance = abs(point1[0] - point2[0])
    y_distance = abs(point1[1] - point2[1])
    distance = math.sqrt(x_distance**2 + y_distance**2)
    return distance

class Population:
    def __init__(self):
        pass

    def setupIndividuals(self, individuals):
        self.individuals = individuals

    def newDay(self):
        self.added_individuals = 0
        self.minus_individuals = 0
        self.killed_individuals = 0
        for individual in self.individuals:
            individual.nutrition -= 1
            if individual.nutrition < individual.survival_nutrition:
                individual.kill()
                return
            if individual.kill_nutrition <= individual.replication_nutrition:
                if random.randrange(100) < individual.violence:
                    if individual.nutrition >= individual.kill_nutrition:
                        individual.killOtherIndividual()
                else:    
                    if individual.nutrition >= individual.replication_nutrition:
                        individual.reproduce()
            elif individual.kill_nutrition > individual.replication_nutrition:
                if individual.nutrition >= individual.kill_nutrition:
                    if random.randrange(100) < individual.violence:
                        individual.killOtherIndividual()
                    else:
                        if individual.nutrition >= individual.replication_nutrition:
                            individual.reproduce()
                else:    
                    if individual.nutrition >= individual.replication_nutrition:
                        individual.reproduce()
            else:
                pass


class Individual:
    def __init__(self, traits, population, position, min_nutritions, game_width, game_height):
        self.mutation_rate = traits['mutation_rate']
        self.vision_distance = traits['vision_distance']
        self.eating_distance = traits['eating_distance']
        self.violence = traits['violence']
        self.population = population
        self.position = position
        self.survival_nutrition = min_nutritions['survival_nutrition']
        self.replication_nutrition = min_nutritions['replication_nutrition']
        self.kill_nutrition = min_nutritions['kill_nutrition']
        self.min_nutritions = min_nutritions
        self.nutrition = 0
        self.food_to_be_eaten = None
        self.game_width = game_width
        self.game_height = game_height

    def kill(self):
        self.population.individuals.remove(self)
        self.population.minus_individuals += 1

    def reproduce(self):
        self.mutating = False

        self.mutation_rate_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.mutation_rate_mutation_bool == True:
            self.mutation_rate_mutation = random.randrange(100)
            self.mutating = True
        else:
            self.mutation_rate_mutation = self.mutation_rate

        self.vision_distance_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.vision_distance_mutation_bool == True:
            self.vision_distance_mutation = random.randrange(200)
            self.mutating = True
        else:
            self.vision_distance_mutation = self.vision_distance

        self.eating_distance_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.eating_distance_mutation_bool == True:
            self.eating_distance_mutation = random.randrange(125)
            self.mutating = True
        else:
            self.eating_distance_mutation = self.eating_distance

        self.violence_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.violence_mutation_bool == True:
            self.violence_mutation = random.randrange(100)
            self.mutating = True
        else:
            self.violence_mutation = self.violence

        self.population.individuals.append(Individual({"mutation_rate": self.mutation_rate_mutation, "vision_distance": self.vision_distance_mutation, "eating_distance": self.eating_distance_mutation, "violence": self.violence_mutation}, self.population, [random.randint(1, self.game_width), random.randint(1, self.game_height)], self.min_nutritions, self.game_width, self.game_height))
        self.population.added_individuals += 1
        self.nutrition -= self.replication_nutrition

    def killOtherIndividual(self):
        for individual in self.population.individuals:
            self.distance = distanceBetween(self.position, individual.position)
            if self.distance <= self.eating_distance:
                del self.population.individuals[self.population.individuals.index(individual)]
                self.population.minus_individuals += 1
                self.population.killed_individuals += 1

    def determineNextPosition(self, list_of_food):
        self.closest_food = Food((99999999999999999, 99999999999999999999, 99999999999999999), 0)
        self.list_of_food = list_of_food
        self.foods_able_to_be_travelled_to = []
        for food in self.list_of_food:
            self.distance = distanceBetween(self.position, food.position)
            if self.distance <= self.vision_distance:
                self.foods_able_to_be_travelled_to.append(food)
        if len(self.foods_able_to_be_travelled_to) != 0:
            for food in self.foods_able_to_be_travelled_to:
                if self.closest_food.position > food.position:
                    self.closest_food = food
            return self.closest_food.position
        else:
            return self.position

        return (self.x, self.y)

    def eatFood(self, list_of_food):
        self.list_of_food = list_of_food
        self.foods_able_to_be_eaten = []
        for food in self.list_of_food:
            self.distance = distanceBetween(self.position, food.position)
            if self.distance <= self.eating_distance:
                self.foods_able_to_be_eaten.append(food)
        if len(self.foods_able_to_be_eaten) != 0:
            for food in self.foods_able_to_be_eaten:
                self.food_to_be_eaten = food
                self.nutrition += 1
                del self.list_of_food[self.list_of_food.index(food)]
            return list_of_food
        else:
            self.food_to_be_eaten = None
            return list_of_food


class FoodProducer:
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height

    def produceFood(self, number_of_food):
        self.number_of_food = number_of_food
        self.food_list = []

        for i in range(1, self.number_of_food + 1):
            self.food_list.append(Food((random.randrange(self.game_width), random.randrange(self.game_height)), 1))

        return(self.food_list)


class Food:
    def __init__(self, position, nutrition):
        self.position = position
        self.nutrition = nutrition
