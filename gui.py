import evolution, pygame, random, time

def run():
    game_width = int(input("What width, in pixels, should the game window be? "))
    game_height = int(input("What height, in pixels, should the game window be? "))
    screen = pygame.display.set_mode((game_width, game_height))
    pygame.display.set_caption("Evolution Simulator")

    STARTING_POPULATION_NUMBER = int(input("How many creatures would you like to spawn on the first day? "))
    population = []
    pop = evolution.Population()
    for i in range(1, STARTING_POPULATION_NUMBER + 1):
        population.append(evolution.Individual({"mutation_rate": 10, "vision_distance": 75, "eating_distance": 50, "violence": 10}, pop, [random.randrange(game_width), random.randrange(game_height)], {"survival_nutrition": 1, "replication_nutrition": 3, "kill_nutrition": 2}, game_width, game_height))
    pop.setupIndividuals(population)

    individuals_positions = []
    for individual in pop.individuals:
        while individual.position in individuals_positions:
            individual.position = [random.randrange(game_width), random.randrange(game_height)]
        individuals_positions.append(individual.position)

    NUMBER_OF_FOOD = int(input("How much food would you like to spawn per day? "))

    food_producer = evolution.FoodProducer(game_width, game_height)
    food = []

    time_per_day = float(input("How many seconds would you like each day to take? "))
    gameplay = input("Would you like the game to automatically go through the turns, or do you want to manually start each turn? (answer with 'automatic' or 'manual') ")

    running = True
    day = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        
        individual_count = 0
        food += food_producer.produceFood(NUMBER_OF_FOOD)
        for food_item in food:
            pygame.draw.circle(screen, (0, 0, 0), food_item.position, 5)
        for individual in pop.individuals:
            food = individual.eatFood(food)
            next_position = individual.determineNextPosition(food)
            pygame.draw.circle(screen, (round(individual.vision_distance) / 200 * 255, 0, 0), next_position, individual.vision_distance)
            pygame.draw.circle(screen, (0, 0, 255), next_position, individual.eating_distance)
            pygame.draw.circle(screen, (255, 0, 255), next_position, 10)
        
        time.sleep(time_per_day/3)
        pop.newDay()
        time.sleep(time_per_day/3)
        #screen.fill((255, 255, 255))
        for food_item in food:
            pygame.draw.circle(screen, (0, 0, 0), food_item.position, 5)
        for individual in pop.individuals:
            food = individual.eatFood(food)
            next_position = individual.determineNextPosition(food)
            pygame.draw.circle(screen, (round(individual.vision_distance) / 200 * 255, 0, 0), next_position, individual.vision_distance)
            pygame.draw.circle(screen, (0, 0, 255), next_position, individual.eating_distance)
            pygame.draw.circle(screen, (255, 0, 255), next_position, 10)
        
        time.sleep(time_per_day/3)
        pygame.display.update()
        if pop.added_individuals > pop.minus_individuals:
            print("Number of creatures: " + str(len(pop.individuals)) + ". Overall change: +" + str(pop.added_individuals - pop.minus_individuals) + ". Added: " + str(pop.added_individuals) + ". Taken away: " + str(pop.minus_individuals) + ". Killed: " + str(pop.killed_individuals) + ".")
        else:
            print("Number of creatures: " + str(len(pop.individuals)) + ". Overall change: " + str(pop.added_individuals - pop.minus_individuals) + ". Added: " + str(pop.added_individuals) + ". Taken away: " + str(pop.minus_individuals) + ". Killed: " + str(pop.killed_individuals) + ".")
        print("Creature stats:")
        for individual in pop.individuals:
            print("Creature Number " + str(pop.individuals.index(individual)))
            print("Vision distance = " + str(individual.vision_distance) + ", eating distance = " + str(individual.eating_distance) + ", position = " + str(individual.position) + ", nutrition = " + str(individual.nutrition))
        print("Day " + str(day) + " finished.")
        if len(pop.individuals) == 0:
            print("Extinction on day " + str(day))
            running = False
        day += 1
        if gameplay == "manual":
            input()

    pygame.quit()
    
run()

restart = input("Press enter to quit or type 'r' to simulate again. ")

if restart == "r":
    run()
