import customtkinter
import heapq
import tkinter as tk
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys
from tkinter import simpledialog
import random
from collections import deque
from tabulate import tabulate

class MultiInputDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Task:").grid(row=0)
        tk.Label(master, text="Priority:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        return self.e1  # initial focus

    def apply(self):
        self.task = self.e1.get()
        self.priority = self.e2.get()



class TableWidget(QWidget):
    def __init__(self, table_data, parent=None):
        super(TableWidget, self).__init__(parent)
        self.table_data = table_data
        self.initUI()
        self.resize(800, 600)
    def initUI(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(len(self.table_data))
        self.table.setColumnCount(len(self.table_data[0]))

        for i, row in enumerate(self.table_data):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(cell)))

        # self.table.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class Routify(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # self.root = root
        self.tasks = []
        self.slots = []
        self.days = []
        self.tp = {}
        self.sp = {}

        self.title("Routify")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Routify", font=("California FB", 32, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="About", command=self.About)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.central_label = customtkinter.CTkLabel(self, text="", fg_color="transparent", anchor="center")
        self.central_label.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="New",command=self.NewRoutine)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Help", command=self.Help)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        

    def clear_frame(self):
        for widget in self.central_label.winfo_children():
            widget.destroy()

    

    def NewRoutine(self):
        self.clear_frame()



        self.add_task_button = customtkinter.CTkButton(self.central_label, text="Add Task", command=self.AddTask, hover_color="dark blue", corner_radius=50, anchor="center")
        self.add_task_button.grid(row=1, column=0, padx = (400,400), pady=(20, 0))

        self.add_slot_button = customtkinter.CTkButton(self.central_label, text="Add Slot", command=self.AddSlot, corner_radius=50)
        self.add_slot_button.grid(row=2, column=0, pady=(20, 0))

        self.add_days_button = customtkinter.CTkButton(self.central_label, text="Add Days", command=self.AddDays, hover_color="dark green", corner_radius=50)
        self.add_days_button.grid(row=3, column=0,  pady=(20, 0))

        self.add_routine_button = customtkinter.CTkButton(self.central_label, text="Generate Routine", command=self.CreateRoutine, hover_color="dark blue", corner_radius=50)
        self.add_routine_button.grid(row=4, column=0,pady=(20, 0))

    def AddTask(self):
        self.task = customtkinter.CTkInputDialog(text="Type in a Task[SPACE]Priority:", title="Add Task")
        taskArg = self.task.get_input()
        args = taskArg.split(" ")
        task = args[0]
        task_priority = int(args[1])
        print(task_priority)
        self.tasks.append((-task_priority, task))
        if task_priority not in self.tp:
            self.tp[task] = task_priority
        heapq.heapify(self.tasks)
        self.original_tasks = list(self.tasks)
        
    def AddSlot(self):

        self.time = customtkinter.CTkInputDialog(text="Type in a Time Slot[SPACE]Priority:", title="Add Time Slot")
        timeArg = self.time.get_input()
        args = timeArg.split(" ")
        slot = args[0]
        slot_priority = int(args[1])
        self.slots.append((-slot_priority, slot))
        if slot_priority not in self.sp:
            self.sp[slot] = slot_priority
        heapq.heapify(self.slots)

    
    def AddDays(self):

        self.time = customtkinter.CTkInputDialog(text="Type in a name of Days", title="Add Days")
        timeArg = self.time.get_input()
        args = timeArg.split(" ")
        for i in args:
            self.days.append(i)


    def CreateRoutine(self):
        original_tasks = list(self.tasks)

    # Create a heap from the slots and tasks
        heapq.heapify(self.slots)
        heapq.heapify(self.tasks)

        # Shuffle the days
        random.shuffle(self.days)

        # Create the routine matrix
        matrix = [['0'] + self.days]

        # Create a queue of tasks
        task_queue = deque(original_tasks)

        # Assign tasks to days for each set of slots
        while self.slots:
            slot_priority, slot = heapq.heappop(self.slots)  # Pop slot with highest priority
            row = [slot]
            for _ in self.days:
                if not task_queue:  # If the task queue is empty
                    task_queue = deque(original_tasks)  # Re-populate the task queue
                    random.shuffle(task_queue)  # Shuffle the task queue
                task_priority, task = task_queue.popleft()  # Remove the next task from the front of the queue
                row.append(task)  # Append the task to the row
            matrix.append(row)

        # for row in matrix:
        #     print('\t'.join(str(element) for element in row))

        app = QApplication(sys.argv)
        table_widget = TableWidget(matrix)
        table_widget.show()
        sys.exit(app.exec_())
        print(tabulate(matrix, headers="firstrow", tablefmt="grid"))
        return matrix, self.tp, self.sp


    def About(self):
        self.clear_frame()

    # Create a new CTkLabel widget with the desired text and formatting options
        message_label = customtkinter.CTkLabel(self.central_label, text='''the prob is that it does not take in newline by itself, how to make it such that it starts from extreme left and when the sentence reaches the extreme right a new line is made and it continues that way. Do not use lang that gets filetered pls''', font=("Arial", 20), anchor="center", justify="center",  wraplength=self.central_label.winfo_height())

        # Add the CTkLabel widget to the central_label frame and make it expand to fill the available space
        message_label.pack(expand=True, fill="both")

    def Help(self):
        self.clear_frame()

        # Create a new CTkLabel widget with the desired text and formatting options
        message_label = customtkinter.CTkLabel(self.central_label, text="Task Added Successfully!", font=("Arial", 20))

        # Add the CTkLabel widget to the central_label frame
        message_label.pack()


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

app = Routify()

app.mainloop()