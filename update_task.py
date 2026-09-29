
import tkinter as tk
from tkinter import messagebox
from operations import save_tasks
from validation import validateInput

#this opens a small window so the user can edit a chosen task
def open_edit_popup(task, tasks_list, refresh_current_tasks, reset_selected_task):

    popup = tk.Toplevel()
    popup.title("Edit Task")
    popup.configure(bg="#d1e7f7")
    
    popup_width = 300
    popup_height = 250
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = int((screen_width / 2) - (popup_width / 2))
    y = int((screen_height / 2) - (popup_height / 2))
    popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')

    tk.Label(popup, text="Edit Task", font=("Arial", 16, "bold"), bg="#d1e7f7").pack(pady=10)

    #the input box is pre-filled with the current task name so the user can see what they're changing
    tk.Label(popup, text="Task Title:", bg="#d1e7f7").pack()
    title_input = tk.Entry(popup, font=("Arial", 14), relief="flat")
    title_input.insert(0, task["task_title"])
    title_input.pack(pady=5)

    #dropdown pre-set to the current priority
    priority_choice = tk.StringVar(value=task["task_priority"])
    priority_menu = tk.OptionMenu(popup, priority_choice, "High", "Medium", "Low")
    priority_menu.config(relief="flat",
                        bg="white",
                        fg="#666666")
    priority_menu.pack(pady=5)

    def save_changes(event=None):
        new_title = title_input.get().strip()
        new_priority = priority_choice.get()

        #only saves if the user didnt leave the title empty
        if validateInput(new_title, tasks_list):
            task["task_title"] = new_title
            task["task_priority"] = new_priority

            save_tasks(tasks_list)
            reset_selected_task()
            refresh_current_tasks()
            messagebox.showinfo("Success", "Task updated successfully!")
            popup.destroy()

    tk.Button(popup, text="Save", command=save_changes, bg="white",
              fg="#666666", font=("Arial", 12), relief="flat").pack(pady=10)


#BINDS DOUBLE CLICK TO EACH TASK BLOCK
def bind_double_click(task_block, task, tasks_list, refresh_current_tasks, reset_selected_task):
    """Connects double click event to popup and all children labels (title, priority)"""

    #this locks in which task was clicked so the popup knows what to edit
    def on_double_click(event, current_task=task):
        open_edit_popup(current_task, tasks_list, refresh_current_tasks, reset_selected_task)

    #this binds to the frame and its labels so clicking anywhere on the task works
    task_block.bind("<Double-Button-1>", on_double_click)
    
    for child in task_block.winfo_children():
        if not isinstance(child, tk.Checkbutton):
            child.bind("<Double-Button-1>", on_double_click)