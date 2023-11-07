# materials

Chore Assignment Application
Introduction
This Chore Assignment Application is a user-friendly tool designed to fairly distribute house chores among a group of people. The distribution is based on individual ratings for each chore's difficulty to ensure an "envy-free" allocation, where no person prefers another's set of chores over their own. The application uses a simple GUI built with Tkinter and applies a Monte Carlo method to find a suitable chore distribution.
Features
Collects user inputs for the number of participants and chores.
Allows each participant to rate the difficulty of each chore privately.
Implements a Monte Carlo simulation to ensure an envy-free distribution of chores.
Exports the final chore assignments to a text file.
Installation
No installation is necessary. The application is a standalone Python script that requires Python to be installed on your system. You can download Python from the official website.
Usage
To run the application, execute the script in a Python environment. The GUI will guide you through the input process:
Run the script using your Python interpreter:
shCopy codepython chore_assignment_app.py
Input the number of people and chores as prompted by the application.
Each person will be asked to rate the difficulty of each chore on a scale from 1 to 10.
After all ratings are collected, the application will attempt to find an envy-free distribution.
If no such distribution is found initially, chore frequencies will be doubled and the process repeated.
The final chore assignments will be displayed to each participant and saved to a text file named "Chores distribution.txt" in the script's directory.
