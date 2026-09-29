from tkinter import messagebox

#Input validation function to check the task inputted is correct
def validateInput(task_title, tasks_list):
    #Stores the task inputted from the entry box
    task_title = task_title.strip()

    #Popup to display if there is an empty string
    if task_title == "":
        messagebox.showerror("Error", "Task cannot be empty!")
        return False # data is not saved
    
    #Popup to display that there is too many characters
    if len(task_title) > 100:
        messagebox.showerror("Error", "Task cannot exceed 100 characters!")
        return False # data is not saved
    
    #Popup to display a task already exists
    for task in tasks_list:
        if task["task_title"].lower() == task_title.lower():
            messagebox.showerror("Error", "Task already exists!")
            return False # data is not saved
    
    return True # data is validated and saved