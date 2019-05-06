import random, math

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
        for individual in self.individuals:
            individual.nutrition -= 1
            if individual.nutrition < individual.survival_nutrition:
                individual.kill()
            if individual.kill_nutrition <= individual.replication_nutrition:
                if random.randrange(100) < individual.violence:
                    if individual.nutrition >= individual.kill_nutrition:
                        individual.killIndividual()
                else:    
                    if individual.nutrition >= individual.replication_nutrition:
                        individual.replicate()
            elif individual.kill_nutrition > individual.replication_nutrition:
                if individual.nutrition >= individual.kill_nutrition:
                    if random.randrange(100) < individual.violence:
                        individual.killIndividual()
                    else:
                        if individual.nutrition >= individual.replication_nutrition:
                            individual.replicate()
                else:    
                    if individual.nutrition >= individual.replication_nutrition:
                        individual.replicate()
            else:
                pass


class Individual:
    def __init__(self, traits, population, position, min_nutritions):
        self.mutation_rate = traits['mutation_rate']
        self.vision_distance = traits['vision_distance']
        self.violence = traits['violence']
        self.population = population
        self.position = position
        self.survival_nutrition = min_nutritions['survival_nutrition']
        self.replication_nutrition = min_nutritions['replication_nutrition']
        self.kill_nutrition = min_nutritions['kill_nutrition']
        self.min_nutritions = min_nutritions
        self.nutrition = 0
        self.food_to_be_eaten = None

    def kill(self):
        self.population.individuals.remove(self)
        self.population.minus_individuals += 1

    def replicate(self):
        self.mutating = False
        self.mutation_rate_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.mutation_rate_mutation_bool == True:
            self.mutation_rate_mutation = random.randrange(100)
            self.mutating = True
        else:
            self.mutation_rate_mutation = self.mutation_rate
        self.vision_distance_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.vision_distance_mutation_bool == True:
            self.vision_distance_mutation = random.randrange(100)
            self.mutating = True
        else:
            self.vision_distance_mutation = self.vision_distance
        self.violence_mutation_bool = random.randrange(100) < self.mutation_rate
        if self.violence_mutation_bool == True:
            self.violence_mutation = random.randrange(100)
            self.mutating = True
        else:
            self.violence_mutation = self.violence
        self.population.individuals.append(Individual({"mutation_rate": self.mutation_rate_mutation, "vision_distance": self.vision_distance_mutation, "violence": self.violence_mutation}, self.population, self.position, self.min_nutritions))
        self.population.added_individuals += 1
        self.nutrition -= self.replication_nutrition

    def killIndividual(self):
        for individual in self.population.individuals:
            self.distance = distanceBetween(self.position, individual.position)
            if self.distance <= self.vision_distance:
                del self.population.individuals[self.population.individuals.index(individual)]
                self.population.minus_individuals += 1

    def determineNextPosition(self):
        if self.food_to_be_eaten == None:
            self.x = self.position[0]
            self.y = self.position[1]
        else:
            self.x = self.food_to_be_eaten.position[0]
            self.y = self.food_to_be_eaten.position[1]
        self.position = [self.x, self.y]

        return (self.x, self.y)

    def eatFood(self, list_of_food):
        self.list_of_food = list_of_food
        self.foods_able_to_be_eaten = []
        for food in list_of_food:
            self.distance = distanceBetween(self.position, food.position)
            if self.distance <= self.vision_distance:
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
    def __init__(self):
        pass

    def produceFood(self, number_of_food):
        self.number_of_food = number_of_food
        self.food_list = []

        for i in range(1, self.number_of_food + 1):
            self.food_list.append(Food((random.randrange(800), random.randrange(500)), 1))

        return(self.food_list)


class Food:
    def __init__(self, position, nutrition):
        self.position = position
        self.nutrition = nutrition
