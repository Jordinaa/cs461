# Author: Jordan Taranto
import random
import numpy as np
from data import NUM_SCHEDULES, NUM_GENERATIONS, MUTATION_RATE, TIME_SLOTS, ROOMS, ACTIVITIES, FACILITATORS

# initlizing population 
def create_random_schedule():
    return [
        {
            "activity": activity,
            "room": random.choice(list(ROOMS.keys())),
            "time": random.choice(TIME_SLOTS),
            "facilitator": random.choice(FACILITATORS)
        }
        for activity in ACTIVITIES
    ]

def initialize_population():
    return [create_random_schedule() for _ in range(NUM_SCHEDULES)]

def calculate_fitness(schedule):
    fitness = 0
    facilitator_load = {fac: 0 for fac in FACILITATORS}
    room_time_usage = {}
    TIME_SLOT_INDEX = {time: idx for idx, time in enumerate(TIME_SLOTS)}

    for entry in schedule:
        activity, room, time, facilitator = entry.values()
        enrollment, preferred, others = ACTIVITIES[activity]
        room_size = ROOMS[room]

        # size of room check 
        if room_size >= enrollment and room_size <= 3 * enrollment:
            fitness += 0.3  
        else:
            fitness -= 0.3  

        # facil. preference 
        if facilitator in preferred:
            fitness += 0.5
        elif facilitator in others:
            fitness += 0.2
        else:
            fitness -= 0.1

        # track the facil. load
        facilitator_load[facilitator] += 1

        # room and time conflict gives penalty 
        if (room, time) in room_time_usage:
            fitness -= 0.5  
        else:
            room_time_usage[(room, time)] = activity

    # penalizes for low and high loead
    for load in facilitator_load.values():
        if load == 1:
            fitness -= 0.4  
        elif load > 4:
            fitness -= 0.5

    # time slot checker kind of 
    sections = {"SLA101A", "SLA101B", "SLA191A", "SLA191B"}
    section_times = {sec: [e["time"] for e in schedule if e["activity"] == sec] for sec in sections}

    # difference between pairs 
    for sec1, sec2 in [("SLA101A", "SLA101B"), ("SLA191A", "SLA191B")]:
        if len(section_times[sec1]) == len(section_times[sec2]) == 1:
            time_diff = abs(TIME_SLOT_INDEX[section_times[sec1][0]] - TIME_SLOT_INDEX[section_times[sec2][0]])
            fitness += 0.5 if time_diff > 4 else -0.5 if time_diff == 0 else 0

    return fitness

# selection
# crossover
# mutation 
def select_parents(population):
    fitness_scores = [calculate_fitness(schedule) for schedule in population]
    probabilities = np.exp(fitness_scores) / np.sum(np.exp(fitness_scores))
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

def crossover(parent1, parent2):
    split_point = random.randint(1, len(ACTIVITIES) - 1)
    child1 = parent1[:split_point] + parent2[split_point:]
    child2 = parent2[:split_point] + parent1[split_point:]
    return [child1, child2]

def mutate(schedule, mutation_rate):
    for entry in schedule:
        if random.random() < mutation_rate:
            entry["room"] = random.choice(list(ROOMS.keys()))
            entry["time"] = random.choice(TIME_SLOTS)
            entry["facilitator"] = random.choice(FACILITATORS)
    return schedule

# the genetic algorithim calling each function 
def genetic_algorithm():
    population = initialize_population()
    for generation in range(NUM_GENERATIONS):
        next_population = []
        for _ in range(NUM_SCHEDULES // 2):
            parent1, parent2 = select_parents(population)
            offspring = crossover(parent1, parent2)
            next_population.extend([mutate(child, MUTATION_RATE) for child in offspring])

        # update population to next
        population = next_population

        # calculate fitness 
        fitness_scores = [calculate_fitness(schedule) for schedule in population]
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}, Best Fitness: {best_fitness}")

        with open("output.txt", "a") as file:
            file.write(f"Generation {generation}, Best Fitness: {best_fitness}\n")
        
        # adjust the mutation rate
        global MUTATION_RATE
        if generation > 0 and max(fitness_scores) - best_fitness < 0.01 * best_fitness:
            MUTATION_RATE /= 2

    best_schedule = max(population, key=calculate_fitness)
    return best_schedule

