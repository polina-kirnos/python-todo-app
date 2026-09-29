"""This module contains GUI operations/logic,
basically what happends with data when user interacts with application interface"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from operations import save_tasks, add_task, remove_task, sort_by_priority, sort_by_title
from validation import validateInput

# GUI core functions
def update_task_status(task, task_status, tasks_list, refresh_current_tasks):
    # get the (current loop iteration) task and save it to JSON
    task["task_completed"] = task_status.get()

    updated_tasks_list = sort_by_priority(tasks_list)
    tasks_list.clear()
    tasks_list.extend(updated_tasks_list)

    save_tasks(tasks_list)
    refresh_current_tasks()
    
"""Functions must always loop through tasks and automatically update displayed tasks when changes are made"""

# defining a function which takes key and a value 
def add_new_task(entry_task_title, var_priority, var_colour, tasks_list, refresh_current_tasks):
    # getting values from user's input/choices
    title = entry_task_title.get().strip()
    priority = var_priority.get()
    # if priority not selected by user, set it to "Medium"
    if priority == "Priority":
        priority = "Medium"
    
    colour = var_colour.get()
    # task colour not selected by user, set task background to blue
    if colour == "Colour":
        colour = "Blue"

    # task title validation
    if validateInput(title, tasks_list):
        add_task(tasks_list, title, priority, colour)
        # in input is valid, tasks is added and automatically sorted by priority
        tasks_sort_by_priority(tasks_list, refresh_current_tasks)
        # clear the input box so user can type in new task
        entry_task_title.delete(0, "end")
        # reset the "Priority" and "Colour" menus
        var_priority.set("Priority")
        var_colour.set("Colour")

        refresh_current_tasks()

# applying sorting functions by using the sorting logic and updating the all tasks list"""
def tasks_sort_by_priority(tasks_list, refresh_current_tasks):
    """Sort tasks by priority and update the all tasks list"""
    sorted_tasks_list = sort_by_priority(tasks_list)
    # to avoid duplicates, sort all tasks and save into a separate list
    # then clear the tasks list and extend new one
    # extend iterates through each item in the list
    # unlike append() that results in nested lists
    tasks_list.clear()
    tasks_list.extend(sorted_tasks_list)
    refresh_current_tasks()

def tasks_sort_by_title(tasks_list, refresh_current_tasks):
    """Sort tasks in aplhabetical order and update the all tasks list"""
    sorted_tasks_list = sort_by_title(tasks_list)
    tasks_list.clear()
    tasks_list.extend(sorted_tasks_list)
    refresh_current_tasks()

def delete_selected_task(tasks_list, selected_task_id, refresh_current_tasks):
    """To delete a task user clicks on task, then presses "DELETE" button"""
    if selected_task_id is not None:
        remove_task(tasks_list, selected_task_id)
        selected_task_id = None
        refresh_current_tasks()
    else:
        # program must inform the user if they did not select a task to be deleted but pressed the "DELETE" button
        messagebox.showwarning("Warning!", "Please select a task to delete.")

def clear_completed_tasks(tasks_list, refresh_current_tasks):
    """Filters task based on "task_completed", if True - such task is removed"""
    new_tasks_list = [task for task in tasks_list if not task.get("task_completed", False)]
    tasks_list.clear()
    tasks_list.extend(new_tasks_list)
    save_tasks(tasks_list)
    refresh_current_tasks()