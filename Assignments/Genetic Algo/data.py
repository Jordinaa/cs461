# Author: Jordan Taranto

# constant variables 
NUM_SCHEDULES = 500
NUM_GENERATIONS = 100
MUTATION_RATE = 0.01
TIME_SLOTS = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

ROOMS = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60
}

ACTIVITIES = {
    "SLA100A": (50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
    "SLA100B": (50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
    "SLA191A": (50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
    "SLA191B": (50, ["Glen", "Lock", "Banks", "Zeldin"], ["Numen", "Richards"]),
    "SLA201": (50, ["Glen", "Banks", "Zeldin", "Shaw"], ["Numen", "Richards", "Singer"]),
    "SLA291": (50, ["Lock", "Banks", "Zeldin", "Singer"], ["Numen", "Richards", "Shaw", "Tyler"]),
    "SLA303": (60, ["Glen", "Zeldin", "Banks"], ["Numen", "Singer", "Shaw"]),
    "SLA304": (25, ["Glen", "Banks", "Tyler"], ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"]),
    "SLA394": (20, ["Tyler", "Singer"], ["Richards", "Zeldin"]),
    "SLA449": (60, ["Tyler", "Singer", "Shaw"], ["Zeldin", "Uther"]),
    "SLA451": (100, ["Tyler", "Singer", "Shaw"], ["Zeldin", "Uther", "Richards", "Banks"])
}

FACILITATORS = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]
