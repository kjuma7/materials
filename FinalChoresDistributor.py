import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import random
import os

def calculate_difficulty(person, chores_assigned, ratings):
    return sum(ratings[person][chore["name"]] for chore in chores_assigned)

def is_assignment_envy_free(assignment, ratings, persons):
    for person in persons:
        own_difficulty = calculate_difficulty(person, assignment[person], ratings)
        for other_person in persons:
            if person != other_person:
                other_difficulty = calculate_difficulty(person, assignment[other_person], ratings)
                if own_difficulty > other_difficulty:
                    return False
    return True

def display_disclaimer_and_proceed(person):
    window = tk.Toplevel()
    window.title("Disclaimer")
    tk.Label(window, text=f"Only {person} can view the ratings.").pack(pady=10)
    proceed_button = tk.Button(window, text="Proceed", command=window.destroy)
    proceed_button.pack(pady=10)
    window.grab_set()  # Modal window
    window.wait_window()  # Wait for the user to close the window

def export_chore_assignments(assignment, filename="Chores distribution.txt"):
    with open(filename, "w") as file:
        for person, chores in assignment.items():
            file.write(f"{person} is assigned:\n")
            for chore in chores:
                file.write(f" - {chore['name']}\n")
            file.write("\n")
    messagebox.showinfo("Export Complete", f"Chore assignments have been saved to file: {filename}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get the number of persons and chores using dialogs
    num_persons = simpledialog.askinteger("Input", "Enter the number of persons:", minvalue=1)
    persons = [simpledialog.askstring("Input", f"Enter the name of Person {i + 1}:") for i in range(num_persons)]

    num_chores = simpledialog.askinteger("Input", "Enter the number of chores:", minvalue=1)
    chores = []
    for i in range(num_chores):
        chore_name = simpledialog.askstring("Input", f"Enter the name of Chore {i + 1}:")
        chore_frequency = simpledialog.askinteger("Input", f"Enter the frequency for {chore_name}:", minvalue=1)
        chores.append({"name": chore_name, "frequency": chore_frequency})

    # Get difficulty ratings from each person with a disclaimer before each
    ratings = {}
    for person in persons:
        display_disclaimer_and_proceed(person)
        ratings[person] = {}
        for chore in chores:
            difficulty = simpledialog.askinteger(
                "Input",
                f"Rate the difficulty of {chore['name']} for {person} (1-10, where 1 is easy and 10 is difficult):",
                minvalue=1, maxvalue=10
            )
            ratings[person][chore["name"]] = difficulty

    # Envy-free allocation using Monte Carlo
    best_assignment = None
    multipliers = 0
    while best_assignment is None:
        for _ in range(10000):  # 10,000 random assignments; adjust as necessary
            random_assignment = {person: [] for person in persons}
            random_chores = [chore for chore in chores for _ in range(chore['frequency'])]
            random.shuffle(random_chores)
            for i, chore in enumerate(random_chores):
                random_assignment[persons[i % num_persons]].append(chore)

            if is_assignment_envy_free(random_assignment, ratings, persons):
                best_assignment = random_assignment
                break

        if best_assignment is None:
            # If no envy-free assignment is found, double the frequency of each chore
            for chore in chores:
                chore['frequency'] *= 2
            multipliers += 1

    # Display chore assignments and difficulties for the best assignment
    for person in persons:
        person_chores = best_assignment[person]
        message = f"{person} is assigned: {', '.join([chore['name'] for chore in person_chores])}\n"
        message += f"{person}'s own difficulty: {calculate_difficulty(person, person_chores, ratings)}\n"
        for other_person in persons:
            if person != other_person:
                message += (
                    f"{other_person}'s difficulty from {person}'s perspective: "
                    f"{calculate_difficulty(person, best_assignment[other_person], ratings)}\n"
                )
        messagebox.showinfo("Chore Assignment", message)

    if multipliers > 0:
        messagebox.showinfo("Disclaimer",
                            f"The chore frequencies were doubled {multipliers} time(s) to find an envy-free distribution.")

    # Export chore assignments to a text file
    export_chore_assignments(best_assignment)

    root.mainloop()

if __name__ == "__main__":
    main()
