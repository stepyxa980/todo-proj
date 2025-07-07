from datetime import datetime
import json

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
                        print("Ошибка: Не удается восстановить данные")
                        self._tasks = []
                else:
                    print("Неверный формат данных в файле")
                    self._tasks = []
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Ошибка: Файл поврежден, данные не загружены")
        except Exception as e:
            print(f"Неизвестная ошибка: {str(e)}")


if __name__ == "__main__":
    t_manager = TaskManager()
    t_manager.read_json()
    t_manager.display()
    while True:
        try:
            print("""
0 - Exit
1 - Add task
2 - Remove task
3 - Complete task
4 - See task
5 - Save file
""")
            choice = input(">>>")
            match(choice):
                case '0':
                    break
                case '1':
                    description = input("Enter your task: ")
                    t_manager.add_task(description)
                case '2':
                    try:
                        task_number = int(input("Task number to delete: "))
                        t_manager.remove_task(task_number)
                    except ValueError:
                        print("Ошибка: Введите число!")
                case '3':
                    try:
                        task_number = int(input("Task number to complete: "))
                        t_manager.complete_task(task_number )
                    except ValueError:
                        print("Ошибка: Введите число!")
                case '4':
                    t_manager.display()
                    input()
                case '5':
                    t_manager.write_in_json()
        except:
            pass
