# Author: Jordan Taranto
from algo import genetic_algorithm

# main function to run code 
if __name__ == "__main__":
    best_schedule = genetic_algorithm()
    for entry in best_schedule:
        print(entry)