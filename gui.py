import evolution, pygame, random, time

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Evolution Simulator")

STARTING_POPULATION_NUMBER = int(input("How many creatures would you like to spawn on the first day? "))
population = []
pop = evolution.Population()
for i in range(1, STARTING_POPULATION_NUMBER + 1):
    population.append(evolution.Individual({"mutation_rate": 10, "vision_distance": 50, "violence": 10}, pop, [random.randrange(800), random.randrange(500)], {"survival_nutrition": 1, "replication_nutrition": 2, "kill_nutrition": 2}))
pop.setupIndividuals(population)

individuals_positions = []
for individual in pop.individuals:
    while individual.position in individuals_positions:
        individual.position = [random.randrange(800), random.randrange(500)]
    individuals_positions.append(individual.position)

NUMBER_OF_FOOD = int(input("How much food would you like to spawn per day? "))

food_producer = evolution.FoodProducer()
food = []

time_per_day = float(input("How many seconds would you like each day to take? "))

running = True
day = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    individual_count = 0
    food += food_producer.produceFood(NUMBER_OF_FOOD)
    for individual in pop.individuals:
        food = individual.eatFood(food)
        next_position = individual.determineNextPosition()
        pygame.draw.circle(screen, (round(individual.vision_distance) / 100 * 255, 0, 0), next_position, individual.vision_distance)
        pygame.draw.circle(screen, (255, 0, 255), next_position, 10)
        #next_position = None
    for food_item in food:
        pygame.draw.circle(screen, (0, 0, 0), food_item.position, 5)
    time.sleep(time_per_day/3)
    pop.newDay()
    time.sleep(time_per_day/3)
    #screen.fill((255, 255, 255))
    for individual in pop.individuals:
        food = individual.eatFood(food)
        pygame.draw.circle(screen, (round(individual.vision_distance) / 100 * 255, 0, 0), next_position, individual.vision_distance)
        pygame.draw.circle(screen, (255, 0, 255), next_position, 10)
    for food_item in food:
        pygame.draw.circle(screen, (0, 0, 0), food_item.position, 5)
    time.sleep(time_per_day/3)
    pygame.display.update()
    if pop.added_individuals > pop.minus_individuals:
        print("Number of creatures: " + str(len(pop.individuals)) + ". Overall change: +" + str(pop.added_individuals - pop.minus_individuals) + ". Added: " + str(pop.added_individuals) + ". Taken away: " + str(pop.minus_individuals) + ".")
    else:
        print("Number of creatures: " + str(len(pop.individuals)) + ". Overall change: " + str(pop.added_individuals - pop.minus_individuals) + ". Added: " + str(pop.added_individuals) + ". Taken away: " + str(pop.minus_individuals) + ".")
    print("Day " + str(day) + " finished.")
    if len(pop.individuals) == 0:
        print("Extinction on day " + str(day))
        running = False
    day += 1

pygame.quit()
