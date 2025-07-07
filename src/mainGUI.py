from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk, scrolledtext

class TaskManager:
    def __init__(self):
        self._tasks = []

    def add_task(self, description: str) -> None:

        form_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._tasks.append({
            'time': form_time,
            'description': description,
            'done': False
            })

    def remove_task(self, task_id: int):
        try:
            del self._tasks[task_id-1]
        except IndexError:
            raise ValueError(f"Invalid task ID: {task_id}")

    def complete_task(self, task_id: int):
        try:
            self._tasks[task_id-1]['done'] = True
        except IndexError:
            raise ValueError(f"Invalid task ID: {task_id}")

    def display(self) -> None:
        for n, i in enumerate(self._tasks):
            status = '@' if i['done'] else ' '
            print(f"\n{i['time']}\n№ {n+1} Task: {i['description']}  [{status}]")


    def write_in_json(self) -> None:
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(self._tasks, file, indent=4, ensure_ascii=False)

    def read_json(self) -> None:
        try:
            with open("data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                
                if isinstance(data, list):
                    self._tasks = data
                elif isinstance(data, str):
                    try:
                        self._tasks = json.loads(data)
                    except json.JSONDecodeError:
                        print("Error: Unable to recover data")
                        self._tasks = []
                else:
                    print("Invalid data format in file")
                    self._tasks = []
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error: File is corrupted, data not loaded")
        except Exception as e:
            print(f"Unknown error: {str(e)}")

'''Warning TaskManagerGUI was written by Ai! Due to my inability to use GUI
                            Comments in Russian'''
class TaskManagerGUI:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x500")
        
        self.manager.read_json()
        self.create_widgets()
        self.update_task_list()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Фрейм для добавления задач
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="New Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(input_frame, width=50)
        self.task_entry.grid(row=0, column=1, padx=5)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_btn = ttk.Button(input_frame, text="Add", command=self.add_task)
        add_btn.grid(row=0, column=2, padx=5)
        
        # Фрейм для управления задачами
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        self.complete_btn = ttk.Button(control_frame, text="Complete Task", command=self.complete_task, state=tk.DISABLED)
        self.complete_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_btn = ttk.Button(control_frame, text="Remove Task", command=self.remove_task, state=tk.DISABLED)
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(control_frame, text="Save", command=self.save_tasks)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        # Список задач
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.task_list = scrolledtext.ScrolledText(
            list_frame, 
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Courier New", 10)
        )
        self.task_list.pack(fill=tk.BOTH, expand=True)
        self.task_list.bind("<Button-1>", self.select_task)
        
        # Статус бар
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status("Ready. Tasks loaded: {}".format(len(self.manager._tasks)))

    def add_task(self):
        description = self.task_entry.get().strip()
        if not description:
            self.update_status("Error: Task description cannot be empty!")
            return
            
        self.manager.add_task(description)
        self.task_entry.delete(0, tk.END)
        self.update_task_list()
        self.update_status("Task added: '{}'".format(description))

    def remove_task(self):
        if not hasattr(self, 'selected_task'):
            return
            
        try:
            task_id = self.selected_task
            description = self.manager._tasks[task_id-1]['description']
            self.manager.remove_task(task_id)
            delattr(self, 'selected_task')
            self.update_task_list()
            self.update_buttons_state()
            self.update_status("Task removed: '{}'".format(description))
        except Exception as e:
            self.update_status("Error: " + str(e))

    def complete_task(self):
        if not hasattr(self, 'selected_task'):
            return
            
        try:
            task_id = self.selected_task
            self.manager.complete_task(task_id)
            self.update_task_list()
            self.update_status("Task marked as complete")
        except Exception as e:
            self.update_status("Error: " + str(e))

    def save_tasks(self):
        try:
            self.manager.write_in_json()
            self.update_status("Tasks saved successfully!")
        except Exception as e:
            self.update_status("Error saving tasks: " + str(e))

    def update_task_list(self):
        self.task_list.config(state=tk.NORMAL)
        self.task_list.delete(1.0, tk.END)
        
        for n, task in enumerate(self.manager._tasks):
            status = '@' if task['done'] else ' '
            task_text = f"{task['time']}\n№ {n+1} Task: {task['description']}  [{status}]\n{'-'*50}\n"
            self.task_list.insert(tk.END, task_text)
        
        self.task_list.config(state=tk.DISABLED)

    def select_task(self, event):
        # Определяем, по какой строке кликнули
        index = self.task_list.index(f"@{event.x},{event.y}")
        line_start = index.split('.')[0] + '.0'
        line_end = index.split('.')[0] + '.end'
        
        # Получаем текст строки
        self.task_list.config(state=tk.NORMAL)
        line_text = self.task_list.get(line_start, line_end)
        self.task_list.config(state=tk.DISABLED)
        
        # Ищем номер задачи в строке
        if "№ " in line_text and "Task:" in line_text:
            try:
                task_id = int(line_text.split("№ ")[1].split(" ")[0])
                self.selected_task = task_id
                self.update_buttons_state()
                self.update_status(f"Selected task: {task_id}")
                return
            except (IndexError, ValueError):
                pass
        
        # Сброс выбора если кликнули не по задаче
        if hasattr(self, 'selected_task'):
            delattr(self, 'selected_task')
        self.update_buttons_state()

    def update_buttons_state(self):
        if hasattr(self, 'selected_task'):
            self.complete_btn.config(state=tk.NORMAL)
            self.remove_btn.config(state=tk.NORMAL)
        else:
            self.complete_btn.config(state=tk.DISABLED)
            self.remove_btn.config(state=tk.DISABLED)

    def update_status(self, message):
        self.status_var.set(message)

    def on_close(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()