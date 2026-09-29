"""This module contains data and JSON operations"""

import tkinter as tk
from tkinter import messagebox
import json
import os

# JSON file where all tasks will be saved permanently
tasks_storage = "tasks.json"

# JSON operations
def load_tasks(): 
    if not os.path.exists(tasks_storage):
        return []                                                   
    try:
        with open(tasks_storage, "r") as File:
            return json.load(File)
    except Exception as e:    
        print(f"Error loading file: {e}")
        return []
    
def save_tasks(tasks_list):
    try:
        with open(tasks_storage, "w") as File:
          json.dump(tasks_list, File, indent=4)
          return True
    except Exception as e:
       print(f"Error saving: {e}")
       return False

# core operations
def add_task(tasks_list, title, priority, colour):
    # setting an ID for each task is more efficient than checking task_title
    # to avoid duplicates it loops through all task ID, finds the max one and adds 1
    max_id = 0
    for task in tasks_list:
        if task["task_id"] > max_id:
            max_id = task["task_id"]

    new_task = {
        "task_id": max_id + 1,
        "task_title": title,
        "task_priority": priority,
        "task_colour": colour,
        "task_completed": False
    }

    tasks_list.append(new_task)
    save_tasks(tasks_list)
    return tasks_list

def remove_task(tasks_list, task_id):
    task_found = False
    for task in tasks_list:
        if task["task_id"] == task_id:
            tasks_list.remove(task)
            task_found = True
            messagebox.showinfo("Deleted", "Task has been removed.")
            break

    if task_found:
        save_tasks(tasks_list)
        return tasks_list
    else:
        messagebox.showerror("Error", "Task ID not found, please try again.")
        return tasks_list

# sorting logic
PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3, "": 4}

def sort_by_priority(tasks_list):
    # tasks in progress need to be displayed first
    tasks_in_progress = [task for task in tasks_list if not task["task_completed"]]
    # all completed tasks need to be displayed after the tasks in progress
    tasks_completed = [task for task in tasks_list if task["task_completed"]]

    # each list need to be sorted
    tasks_in_progress.sort(key=lambda task: PRIORITY_ORDER.get(task["task_priority"], 4))
    tasks_completed.sort(key=lambda task: PRIORITY_ORDER.get(task["task_priority"], 4))

    # after sorting lists are combined
    return tasks_in_progress + tasks_completed

def sort_by_title(tasks_list):
    tasks_in_progress = [task for task in tasks_list if not task["task_completed"]]
    tasks_completed = [task for task in tasks_list if task["task_completed"]]

    tasks_in_progress.sort(key=lambda task: task["task_title"].lower())
    tasks_completed.sort(key=lambda task: task["task_title"].lower())

    return tasks_in_progress + tasks_completed

