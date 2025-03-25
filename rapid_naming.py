import tkinter as tk
import random
import time
import csv
import os

# Sample stimuli (original list)
stimuli_master = ["Apple", "Car", "Chair", "Dog", "Tree", "Red", "Blue", "5", "9", "1"]

# Global variables
response_times = []
correctness = []
stimuli_shown = []  
stimuli = []  # This will be set when the test starts
current_stimulus = ""
start_time = None
attempt_number = 1  

# Check previous attempts
if os.path.exists("results.csv"):
    with open("results.csv", "r") as file:
        attempt_number = sum(1 for _ in file) // 6  

# Function to start/restart the test
def start_test():
    global response_times, correctness, stimuli_shown, stimuli, current_stimulus, start_time, attempt_number
    response_times.clear()
    correctness.clear()
    stimuli_shown.clear()
    stimuli = stimuli_master.copy()  # Reinitialize stimuli
    current_stimulus = ""
    start_time = None
    attempt_number += 1

    # Reset UI
    response_entry.pack(pady=20)
    next_button.pack(pady=20)
    restart_button.pack_forget()
    stimulus_label.config(text="Get Ready...")
    
    root.after(1000, next_stimulus)  # Start after 1 second

# Function to display the next stimulus
def next_stimulus():
    global current_stimulus, start_time
    if stimuli:
        current_stimulus = random.choice(stimuli)
        stimuli_shown.append(current_stimulus)  
        stimulus_label.config(text=current_stimulus)
        start_time = time.time()
    else:
        display_score()  
        #save_results()  # Ensure results are saved after test completion

# Function to handle user response
def record_response(event=None):
    global start_time
    if not current_stimulus:
        return  

    response_time = time.time() - start_time
    user_response = response_entry.get()
    response_entry.delete(0, tk.END)

    response_times.append(round(response_time, 2))
    correctness.append(1 if user_response.lower() == current_stimulus.lower() else 0)

    # Remove stimulus and move to the next one
    stimuli.remove(current_stimulus)
    next_stimulus()

# Save results to a CSV file
'''def save_results():
    file_exists = os.path.exists("results.csv")
    
    with open("results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["Attempt", "Stimulus", "Response Time (s)", "Correctness"])
        
        for i in range(len(response_times)):
            writer.writerow([attempt_number, stimuli_shown[i], response_times[i], correctness[i]])  

        avg_time = round(sum(response_times) / len(response_times), 2) if response_times else 0
        avg_correctness = round((sum(correctness) / len(correctness)) * 100, 2) if correctness else 0

        writer.writerow(["Attempt", "Score", "Avg Time (s)", "Accuracy (%)"])
        writer.writerow([attempt_number, f"{sum(correctness)}/{len(correctness)}", avg_time, avg_correctness])
        writer.writerow([])'''

# Function to display final score
def display_score():
    total_questions = len(correctness)
    score = sum(correctness)
    avg_time = round(sum(response_times) / total_questions, 2) if response_times else 0
    avg_correctness = round((score / total_questions) * 100, 2) if total_questions else 0

    # Display in GUI
    stimulus_label.config(text=f"Test Complete!\nScore: {score}/{total_questions}\n"
                               f"Avg Time: {avg_time} sec\n"
                               f"Accuracy: {avg_correctness}%")
    
    # Print in terminal
    print("\n===== Test Completed =====")
    print(f"Score: {score}/{total_questions}")
    print(f"Average Response Time: {avg_time} sec")
    print(f"Accuracy: {avg_correctness}%")
    print("==========================\n")

    response_entry.pack_forget()  
    next_button.pack_forget()  
    restart_button.pack(pady=20)  

# GUI setup
root = tk.Tk()
root.title("Rapid Naming Task")

stimulus_label = tk.Label(root, text="Press Start to Begin", font=("Helvetica", 32))
stimulus_label.pack(pady=20)

response_entry = tk.Entry(root, font=("Helvetica", 24))
response_entry.pack(pady=20)
response_entry.bind("<Return>", record_response)

next_button = tk.Button(root, text="Start Test", command=start_test, font=("Helvetica", 18))
next_button.pack(pady=20)

restart_button = tk.Button(root, text="Restart Test", command=start_test, font=("Helvetica", 18))

root.mainloop()
