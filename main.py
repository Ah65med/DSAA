import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def put(self, item):
        self.queue.append(item)
        self.queue.sort(reverse=True)

    def get(self):
        return self.queue.pop()

    def empty(self):
        return len(self.queue) == 0


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, end, rows, cols, obstacles):
    if end[0] < 0 or end[1] < 0 or end[0] >= rows or end[1] >= cols:
        return []

    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    iteration_count = 0
    current_item = start
    while not frontier.empty():
        _, current_item = frontier.get()

        if current_item == end:
            break

        if iteration_count > 10000:
            break

        for next_item in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_item = (current_item[0] + next_item[0], current_item[1] + next_item[1])

            if next_item[0] < 0 or next_item[1] < 0 or next_item[0] >= rows or next_item[1] >= cols:
                continue

            new_cost = cost_so_far[current_item] + 1

            if next_item not in obstacles and (
                    next_item not in cost_so_far or new_cost < cost_so_far[next_item]):
                cost_so_far[next_item] = new_cost
                priority = new_cost + heuristic(end, next_item)
                frontier.put((priority, next_item))
                came_from[next_item] = current_item

        iteration_count += 1

    if current_item != end:
        return []

    path = []

    while current_item != start:
        path.append(current_item)
        current_item = came_from[current_item]

    path.append(start)
    path.reverse()

    return path


def are_cells_adjacent(cell1, cell2):
    return (cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 1) or \
        (cell1[1] == cell2[1] and abs(cell1[0] - cell2[0]) == 1)


def is_path_valid(path):
    print(path)
    for i in range(len(path) - 1):
        if not are_cells_adjacent(path[i], path[i + 1]):
            print(path[i], path[i + 1])
            return False
    return True


def generate_random_point(rows, cols):
    return random.randint(0, rows - 1), random.randint(0, cols - 1)


class GamePlay:
    def __init__(self, root, rows, cols):
        self.root = root
        self.cols = cols
        self.rows = rows

        self.start = generate_random_point(self.rows, self.cols)
        self.end = generate_random_point(self.rows, self.cols)
        self.obstacles = []
        self.marked = []

        self.cell_size = 40
        self.is_won = False
        self.tries = 3

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = cols * self.cell_size
        window_height = rows * self.cell_size

        position_top = (screen_height - window_height) // 2
        position_right = (screen_width - window_width) // 2

        self.root.state('normal')
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        self.canvas = tk.Canvas(root, width=cols * self.cell_size, height=rows * self.cell_size, bg='white')
        self.canvas.pack()

        while abs(self.start[0] - self.end[0]) + abs(self.start[1] - self.end[1]) < rows // 2:
            self.end = generate_random_point(self.rows, self.cols)

        while len(self.obstacles) < 10:
            new_obstacle = generate_random_point(self.rows, self.cols)
            if new_obstacle != self.start and new_obstacle != self.end:
                self.obstacles.append(new_obstacle)

        for i in range(rows):
            for j in range(cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill_color = "white"

                if (i, j) in [self.start, self.end] + self.obstacles:
                    if (i, j) == self.start:
                        fill_color = "yellow"
                    elif (i, j) == self.end:
                        fill_color = "orange"
                    else:
                        fill_color = "gray"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, tags=f"rect_{i}_{j}")

        self.canvas.bind("<Button-1>", self.grid_click)
        self.root.bind("<space>", self.space_key_press)

    def grid_click(self, event):
        if self.is_won == True:
            messagebox.showinfo("Warning", "Game has finished already!")
        if self.tries < 1:
            messagebox.showinfo("Warning", "You have no tries left!")
        else:
            i = event.y // self.cell_size
            j = event.x // self.cell_size
            tag = f"rect_{i}_{j}"

            if (i, j) not in self.obstacles:
                if (i, j) in self.marked:
                    if self.is_won != True:
                        if (i, j) == self.start:
                            color = "yellow"
                        elif (i, j) == self.end:
                            color = "orange"
                        else:
                            color = "white"

                        self.canvas.itemconfigure(tag, fill=color)
                        self.marked.remove((i, j))
                else:
                    if self.is_won != True:
                        self.canvas.itemconfigure(tag, fill="blue")
                        self.marked.append((i, j))
            else:
                messagebox.showinfo("Warning", "You hit an obstacle!")

    def space_key_press(self, _):
        if self.start in self.marked:
            self.marked.remove(self.start)
            self.marked = [self.start] + self.marked
        if self.end in self.marked:
            self.marked.remove(self.end)
            self.marked = self.marked + [self.end]

        shortest_path = astar(self.start, self.end, self.rows, self.cols, self.obstacles)

        if (((self.marked[0] == self.start and self.marked[-1] == self.end)
             or (self.marked[0] == self.end and self.marked[-1] == self.start))
                and len(self.marked) == len(shortest_path) and is_path_valid(self.marked)):
            self.is_won = True
            for point in self.marked:
                tag = f"rect_{point[0]}_{point[1]}"
                self.canvas.itemconfigure(tag, fill="green")
            messagebox.showinfo("Won", "You found shortest path!")
        elif not shortest_path:
            messagebox.showinfo("No Path", "No path found!")
        else:
            self.tries = self.tries -1

            if len(self.marked) != len(shortest_path):
                if self.tries < 1:
                    for point in self.marked:
                        tag = f"rect_{point[0]}_{point[1]}"
                        self.canvas.itemconfigure(tag, fill="red")
                    for point in shortest_path:
                        tag = f"rect_{point[0]}_{point[1]}"
                        self.canvas.itemconfigure(tag, fill="green")
                    messagebox.showinfo("Lost", "You did not find shortest path!")
                else: 
                    for point in self.marked:
                        tag = f"rect_{point[0]}_{point[1]}"
                        self.canvas.itemconfigure(tag, fill="white")
                    for point in shortest_path:
                        tag = f"rect_{point[0]}_{point[1]}"
                        self.canvas.itemconfigure(tag, fill="white")

                    self.marked = []
                    shortest_path = []

                    tag = f"rect_{self.start[0]}_{self.start[1]}"
                    self.canvas.itemconfigure(tag, fill="yellow")
                    tag = f"rect_{self.end[0]}_{self.end[1]}"                    
                    self.canvas.itemconfigure(tag, fill="orange")

                    messagebox.showinfo("Try Again", f"You did not find shortest path!\nYou have {self.tries} tries left")
            else:
                messagebox.showinfo("Lost", "You skipped a cell!")


class GamePractice:
    def __init__(self, master, rows, cols):
        self.root = master
        self.rows = rows
        self.cols = cols

        self.start = None
        self.end = None
        self.obstacles = []
        self.clicks = 0

        self.cell_size = 40

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = cols * self.cell_size
        window_height = rows * self.cell_size

        position_top = (screen_height - window_height) // 2
        position_right = (screen_width - window_width) // 2

        self.root.state('normal')
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        self.canvas = tk.Canvas(master, width=cols * self.cell_size, height=rows * self.cell_size, bg='white')
        self.canvas.pack()

        for i in range(rows):
            for j in range(cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags=f"rect_{i}_{j}")

        self.canvas.bind("<Button-1>", self.grid_click)
        self.root.bind("<space>", self.space_key_press)

    def grid_click(self, event):
        i = event.y // self.cell_size
        j = event.x // self.cell_size
        tag = f"rect_{i}_{j}"

        if self.clicks == 0:
            self.canvas.itemconfigure(tag, fill='yellow')
            self.start = (i, j)
        elif self.clicks == 1:
            self.canvas.itemconfigure(tag, fill='orange')
            self.end = (i, j)
        elif self.canvas.itemcget(tag, "fill") == "white":
            self.canvas.itemconfigure(tag, fill='gray')
            self.obstacles.append((i, j))

        self.clicks += 1

    def space_key_press(self, _):
        shortest_path = astar(self.start, self.end, self.rows, self.cols, self.obstacles)

        for cell in shortest_path:
            tag = f"rect_{cell[0]}_{cell[1]}"
            current_color = self.canvas.itemcget(tag, "fill")

            if current_color != "gray":
                self.canvas.itemconfigure(tag, fill="green")

        if not shortest_path:
            messagebox.showinfo("No Path", "No path found!")


class Main:
    def __init__(self, root):
        self.root = root
        self.new_window = None

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = screen_width // 2
        window_height = screen_height // 2

        position_top = screen_height // 4
        position_right = screen_width // 4

        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        heading_style = ttk.Style()
        heading_style.configure("Heading.TLabel", foreground="black", font=("Press Start 2P", 32))
        self.heading_label = ttk.Label(root, text="Path Finder", style="Heading.TLabel")
        self.heading_label.pack(pady=10)

        rule4_style = ttk.Style()
        rule4_style.configure("Rule4.TLabel", foreground="black", font=("Press Start 2P", 10))
        self.rule2 = ttk.Label(root, text="Find the shortest path from starting to\n the end point avoiding obstacles",
                               style="Rule4.TLabel")
        self.rule2.pack(pady=3)

        rule3_style = ttk.Style()
        rule3_style.configure("Rule3.TLabel", foreground="gray", font=("Press Start 2P", 10))
        self.rule3 = ttk.Label(root, text="ðŸ”˜ Obstacles", style="Rule3.TLabel")
        self.rule3.pack(pady=3)

        rule1_style = ttk.Style()
        rule1_style.configure("Rule1.TLabel", foreground="yellow", font=("Press Start 2P", 10))
        self.rule1 = ttk.Label(root, text="ðŸ”˜ Starting Point", style="Rule1.TLabel")
        self.rule1.pack(pady=3)

        rule2_style = ttk.Style()
        rule2_style.configure("Rule2.TLabel", foreground="orange", font=("Press Start 2P", 10))
        self.rule2 = ttk.Label(root, text="ðŸ”˜ Ending Point", style="Rule2.TLabel")
        self.rule2.pack(pady=3)

        self.frame_left = tk.Frame(root)
        self.frame_left.pack(side="left", expand=True)

        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side="right", expand=True)

        btn_style = ttk.Style()
        btn_style.configure("Button.TButton", foreground="black", background="white", font=("Press Start 2P", 10))

        self.play_game_btn = ttk.Button(self.frame_left, text="Play", command=self.play_game, style="Button.TButton")
        self.play_game_btn.pack()

        self.practice_game_btn = ttk.Button(self.frame_right, text="Practice", command=self.practice_game,
                                            style="Button.TButton")
        self.practice_game_btn.pack()

    def play_game(self):
        self.root.iconify()
        self.new_window = tk.Toplevel(self.root)
        self.new_window.wm_title("Play Mode")
        GamePlay(self.new_window, 10, 10)
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def practice_game(self):
        self.root.iconify()
        self.new_window = tk.Toplevel(self.root)
        self.new_window.wm_title("Practice Mode")
        GamePractice(self.new_window, 10, 10)
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.root.deiconify()
        self.new_window.destroy()



root = tk.Tk()
root.wm_title("Path Finder")
app = Main(root)
root.mainloop()