"""This module contains app interface layout and is an entry point of the program"""
import tkinter as tk
from tkinter import ttk
import operations as ops
import gui_operations as gui_ops
from update_task import bind_double_click

def select_task(task_id):
    """Since "selected task" more efficient to update as a global variable, this function is kept in main module"""
    global selected_task_id
    # to select a task, user clicks on it
    # to deselect a task, user clicks on the selected task again
    if selected_task_id == task_id:
        selected_task_id = None
    else:
        selected_task_id = task_id
    refresh_current_tasks()

def reset_selected_task():
    """Reset the selected task when user double-clicks of the task to update it"""
    global selected_task_id
    selected_task_id = None
    refresh_current_tasks()

def refresh_current_tasks():
    """Function is heavily connected to the GUI so it is more efficient to keep it in main module, insead of passing a lot of arguments"""
    # clear current displayed tasks in app before updating
    for widget in displayed_tasks_frame.winfo_children():
        widget.destroy()
    
    # loop through the data and create task blocks

    for task in tasks_list:
        # task colour logic: get(user colour, OR default)
        # set default colour to prevent program crashing if user did not set a specific colour
        fill_colour = colour_options.get(task["task_colour"], colour_options["Blue"])

        if task["task_id"] == selected_task_id:
            border_colour = "#E34848"
            border_thickness = 2
        else:
            border_colour = fill_colour # invisible border
            border_thickness = 2

        # add each task box to the frame (explained later in the code)
        task_block = tk.Frame(
            displayed_tasks_frame,
            bg=fill_colour,
            highlightbackground=border_colour,
            highlightthickness=border_thickness,
            padx=10,
            pady=10)
        task_block.pack(fill="x", padx=10, pady=10) # each task block fills all available horizontal space

        # current task status based on toggling the checkbox (either T/F, False by default)
        task_status = tk.BooleanVar(value=task.get("task_completed", False))

        checkbox = tk.Checkbutton(
            task_block,
            variable=task_status, 
            bg=fill_colour, 
            activebackground=fill_colour, 
            highlightthickness=0,
            # applying updating status function to work with checkbox
            # by using t and s we "freeze" current task data
            command=lambda t=task, s=task_status: gui_ops.update_task_status(t, s, tasks_list, refresh_current_tasks))
                                                        
        checkbox.pack(side="left", padx=2)
                                    # to avoid the conflict of single and double clicks, introduce 200ms delay for the signle click to take action
        task_block.bind("<Button-1>", lambda e, task_id=task["task_id"]: window.after(200, lambda: select_task(task_id)))
        title_Label = tk.Label(task_block,
                               text=task["task_title"],
                               font=("Arial", 14, "bold"),
                               bg=fill_colour)
        title_Label.pack(side="left")
        title_Label.bind("<Button-1>",lambda e, task_id=task["task_id"]: window.after(200, lambda: select_task(task_id)))

        priority_Label = tk.Label(task_block,
                                  text=task["task_priority"],
                                  font=("Arial", 12),
                                  bg=fill_colour,
                                  fg="#666666")
        priority_Label.pack(side="right")
        priority_Label.bind("<Button-1>", lambda e, task_id=task["task_id"]: window.after(200, lambda: select_task(task_id)))

        bind_double_click(task_block, task, tasks_list, refresh_current_tasks, reset_selected_task)
        # force the Canvas to recalculate its height every time tasks are refreshed
        displayed_tasks_frame.update_idletasks()
        all_tasks_canvas.config(scrollregion=all_tasks_canvas.bbox("all"))

#load the data first when running the app
tasks_list = ops.load_tasks()
selected_task_id = None

# colour menu options
# structure is colour name: background colour (hex code)
colour_options = {
    "Red": "#FFD2D2",
    "Yellow": "#FFF9A9",
    "Blue": "#C0EDFF",
    "Green": "#C1EAD2",
    "Purple": "#E3D1F2",
    "Pink": "#FFDCF5"
}

# Creating a main window or container to hold all the widgets or buttons, labels etc
window = tk.Tk() 
window.title("To Do List Manager")

# app background
app_background = "#d1e7f7" #separate variable for easier tweaking
window.configure(bg=app_background)

# app window size configuration
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
app_width = int(screen_width * 0.4)
app_height = int(screen_height * 0.8)
# making sure app appear exactly in the centre
# by calculating the coordinates of top left corner
x = int((screen_width / 2) - (app_width / 2))
y = int((screen_height / 2) - (app_height / 2))
window.geometry(f'{app_width}x{app_height}+{x}+{y}')    

# interface layout 
header = tk.Label(window,
                  text="My tasks",
                  font=("Arial", 20, "bold"), 
                  bg="#d1e7f7") 
header.pack(pady=(30, 5)) # vertical asymmetric padding (top, bottom)


# task input bar
input_bar = tk.Frame(window,bg=app_background)
input_bar.pack(fill="x", padx=40, pady=20) # input bar fills the space horizontally

# input field for task title
entry_task_title = tk.Entry(input_bar,
                            font=("Arial", 18),
                            relief="flat") # "flat" removes 90's look from input bar
# expand=True so the task takes all available space from parent widget
entry_task_title.pack(side="left",
                      expand=True,
                      fill="x",
                      padx=(0, 10)) # horizontal asymemtric padding (left, right)

# dropdown menu to select task priority
var_priority = tk.StringVar(value="Priority")
priority_menu = tk.OptionMenu(input_bar, var_priority, "High", "Medium", "Low")
priority_menu.config(width=7,
                    font=("Arial", 12),
                    relief="flat",
                    bg="white",
                    fg="#666666")
# tweaking the drop down menu items
priority_menu["menu"].config(font=("Arial", 12))
priority_menu.pack(side="left", padx=5)

# dropdown menu to select task colour
var_colour = tk.StringVar(value="Colour")
colour_menu = tk.OptionMenu(input_bar, var_colour, *colour_options.keys())
colour_menu.config(width=7,
                   font=("Arial", 12),
                   relief="flat",
                   bg="white",
                   fg="#666666")
colour_menu["menu"].config(font=("Arial", 12))
colour_menu.pack(side="left", padx=5)

# button to add the task
button_add = tk.Button(input_bar,
                       text="+",
                       command=lambda: gui_ops.add_new_task(entry_task_title, var_priority, var_colour, tasks_list, refresh_current_tasks ),
                       bg="white",
                       fg="#666666",
                       font=("Arial", 18),
                       width=3,
                       height=1)
button_add.pack(side="right", padx=5)


# sorting buttons frame
middle_buttons = tk.Frame(window,bg=app_background)
middle_buttons.pack(fill="x", padx=40, pady=10)

# sort tasks by priority button
button_sort_priority = tk.Button(middle_buttons,
                                 text="Sort by Priority",
                                 bg="white",
                                 fg="#666666",
                                 font=("Arial", 12),
                                 command=lambda: gui_ops.tasks_sort_by_priority(tasks_list, refresh_current_tasks))
button_sort_priority.pack(side="left", padx=5, pady=(10, 0))

#sort tasks by title
button_sort_title = tk.Button(middle_buttons,
                              text="Sort by Title",
                              bg="white",
                              fg="#666666",
                              font=("Arial", 12),
                              command=lambda: gui_ops.tasks_sort_by_title(tasks_list, refresh_current_tasks))
button_sort_title.pack(side="left", padx=5, pady=(10, 0))


# need to define bottom buttons first so tasks frame stretches within available space
bottom_buttons = tk.Frame(window, bg=app_background)
bottom_buttons.pack(side="bottom", fill="x", padx=40, pady=20)

# clear completed tasks button so they are not "piling up"
button_clear_completed = tk.Button(bottom_buttons,
                                   text="Clear Completed",
                                   bg="white",
                                   fg="#666666",
                                   font=("Arial", 14),
                                   command= lambda: gui_ops.clear_completed_tasks(tasks_list, refresh_current_tasks))

button_clear_completed.pack(side="left", padx=5, pady=10)

# delete button to remove selected task permanently
button_delete = tk.Button(bottom_buttons,
                          text="DELETE",
                          bg="white",
                          fg="#E34848",
                          font=("Arial", 14),
                          command=lambda: gui_ops.delete_selected_task(tasks_list, selected_task_id, refresh_current_tasks))
button_delete.pack(side="right", padx=5, pady=10)


# main frame that holds tasks scrollable frame and scrollbar
tasks_frame = tk.Frame(window, bg="white")
tasks_frame.pack(fill="both",
                 expand=True,
                 padx=40,
                 pady=5)

# canvas is the only element is standard TKinter that is scrollable
all_tasks_canvas = tk.Canvas(tasks_frame,
                             bg="white",
                             highlightthickness=0)
all_tasks_canvas.pack(side="left",
                      fill="both",
                      expand=True)

scrollbar = ttk.Scrollbar(tasks_frame,
                          orient="vertical",
                          command=all_tasks_canvas.yview)
scrollbar.pack(side="right", fill="y")

# configure the scrollable canvas
all_tasks_canvas.configure(yscrollcommand=scrollbar.set)
# applying function above to the event (e) - scrolling through canvas
all_tasks_canvas.bind("<Configure>", lambda e: all_tasks_canvas.configure(scrollregion=all_tasks_canvas.bbox("all")))

# frame inside canvas that displays tasks as user scrolls through the list
displayed_tasks_frame = tk.Frame(all_tasks_canvas, bg="white")
# as tasks are scrolled through internal frame updates and placed at top right corner of canvas
all_tasks_canvas.create_window((0,0),
                               window=displayed_tasks_frame,
                               anchor="nw",
                               width=int(app_width*0.8))



# run the app
refresh_current_tasks()
window.mainloop()