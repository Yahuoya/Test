import tkinter as tk
from tkinter import messagebox
import random
import time

# 数独生成类
class Sudoku:
    def __init__(self):
        # 初始数独种子
        self.seed = [
            [5, 2, 9, 4, 3, 7, 6, 8, 1],
            [7, 6, 1, 8, 9, 2, 4, 5, 3],
            [3, 8, 4, 6, 1, 5, 2, 7, 9],
            [4, 7, 8, 3, 2, 6, 9, 1, 5],
            [6, 3, 5, 1, 8, 9, 7, 4, 2],
            [9, 1, 2, 5, 7, 4, 3, 6, 8],
            [1, 4, 6, 2, 5, 3, 8, 9, 7],
            [8, 9, 3, 7, 6, 1, 5, 2, 4],
            [2, 5, 7, 9, 4, 8, 1, 3, 6]
        ]
        self.problem = [[0] * 9 for _ in range(9)]  # 初始化空的数独题目
        self.randomlist = self.randomArray()  # 生成随机数组

    def randomArray(self):
        """生成一个包含1到9的随机排列数组。"""
        tmplist = []
        while len(tmplist) < 9:
            ran = random.randrange(1, 10)
            if ran not in tmplist:
                tmplist.append(ran)
        return tmplist

    def createSudoku(self):
        """根据随机排列数组生成数独终盘。"""
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if self.seed[i][j] == self.randomlist[k]:
                        tmp = (k + 1) % 9  # 替换为随机排列中的下一个数字
                        self.seed[i][j] = self.randomlist[tmp]
                        break
        return self.seed

    def remove_numbers(self, grid, difficulty):
        """根据给定难度随机删除数字，生成数独题目。"""
        attempts = difficulty  # 控制空格数量
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while grid[row][col] == 0:  # 找到一个非空的格子
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            grid[row][col] = 0  # 设置为空格
            attempts -= 1
        return grid


# 数独游戏类
class SudokuGame:
    def __init__(self, master):
        """初始化数独游戏界面。"""
        self.master = master
        self.master.title("LYF的数独游戏")
        self.difficulty = 20  # 默认难度（20个空格）
       
        # 创建欢迎界面
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """创建欢迎界面，包含开始游戏、查看规则、选择难度和退出按钮。"""
        for widget in self.master.winfo_children():
            widget.destroy()  # 清空界面

        welcome_label = tk.Label(self.master, text="欢迎来到LYF的数独游戏！", font=("Arial", 24))
        welcome_label.pack(pady=20)

        start_button = tk.Button(self.master, text="开始游戏", font=("Arial", 16), command=self.start_game)
        start_button.pack(pady=10)

        rules_button = tk.Button(self.master, text="游戏规则", font=("Arial", 16), command=self.show_rules)
        rules_button.pack(pady=10)

        difficulty_button = tk.Button(self.master, text="选择难度", font=("Arial", 16), command=self.choose_difficulty)
        difficulty_button.pack(pady=10)

        quit_button = tk.Button(self.master, text="退出游戏", font=("Arial", 16), command=self.master.quit)
        quit_button.pack(pady=10)

    def start_game(self):
        """启动游戏，创建游戏界面。"""
        self.create_game_screen()

    def show_rules(self):
        """显示游戏规则的提示框。"""
        messagebox.showinfo("游戏规则", "1. 每行、每列、每个3x3宫格内，数字1到9不能重复。\n2. 请根据已知数字填入其余数字。\n3. 该数独游戏由92310187522开发，祝您游戏愉快！")

    def choose_difficulty(self):
        """弹出窗口让玩家选择难度，并根据选择设置难度。"""
        def set_difficulty(level):
            if level == '简单模式':
                self.difficulty = 20
            elif level == '中等模式':
                self.difficulty = 30
            elif level == '困难模式':
                self.difficulty = 40
            difficulty_window.destroy()  # 关闭难度选择窗口

        difficulty_window = tk.Toplevel(self.master)
        difficulty_window.title("难度选择")

        easy_button = tk.Button(difficulty_window, text="简单模式", command=lambda: set_difficulty('简单模式'))
        easy_button.pack(pady=5)

        medium_button = tk.Button(difficulty_window, text="中等模式", command=lambda: set_difficulty('中等模式'))
        medium_button.pack(pady=5)

        hard_button = tk.Button(difficulty_window, text="困难模式", command=lambda: set_difficulty('困难模式'))
        hard_button.pack(pady=5)

    def create_game_screen(self):
        """创建游戏界面，生成数独题目并显示输入框。"""
        self.start_time = time.time()  # 记录游戏开始时间
        for widget in self.master.winfo_children():
            widget.destroy()  # 清空欢迎界面

        # 生成数独题目
        sudoku = Sudoku()
        sudoku_grid = sudoku.createSudoku()
        problem_grid = sudoku.remove_numbers([row[:] for row in sudoku_grid], self.difficulty)  # 根据难度删除数字

        self.sudoku_solution = sudoku_grid  # 保存答案用于判断
        self.entries = []

        # 生成数独网格
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(self.master, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=0.1, pady=0.1)
                if problem_grid[i][j] != 0:
                    entry.insert(0, str(problem_grid[i][j]))
                    entry.config(state='disabled')  # 禁止编辑已填入的数字
                row_entries.append(entry)
            self.entries.append(row_entries)

        # 添加功能按钮
        check_button = tk.Button(self.master, text="是否通关？", command=self.check_solution)
        check_button.grid(row=9, column=0, columnspan=2, pady=10)

        reset_button = tk.Button(self.master, text="再来一局！", command=self.create_game_screen)
        reset_button.grid(row=9, column=2, columnspan=2, pady=10)

        quit_button = tk.Button(self.master, text="结束游戏。", command=self.create_welcome_screen)
        quit_button.grid(row=9, column=4, columnspan=2, pady=10)

        show_solution_button = tk.Button(self.master, text="查看答案。", command=self.show_solution)
        show_solution_button.grid(row=9, column=6, columnspan=3, pady=10)
        
    def show_solution(self):
        """查看正确答案"""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0,tk.END)  # 清空玩家输入
                self.entries[i][j].insert(0,str(self.sudoku_solution[i][j]))  #显示正确答案
                self.entries[i][j].config(state='disabled')  # 禁止编辑已填入的数字

    def check_solution(self):
        """检查玩家输入的数独是否正确，增加try-except处理非1到9整数的错误输入。"""
        for i in range(9):
            for j in range(9):
                try:
                    # 获取输入并转换为整数
                    user_input = self.entries[i][j].get()
                    if user_input == "":
                        messagebox.showerror("输入错误", "请填写完所有空格！")
                        return

                    user_input = int(user_input)  # 尝试转换为整数
                    if user_input < 1 or user_input > 9:
                        raise ValueError  # 非1-9的数字视为无效输入

                    # 检查用户输入是否与答案匹配
                    if user_input != self.sudoku_solution[i][j]:
                        messagebox.showerror("错误", "数独填写有误！")
                        return

                except ValueError:
                    messagebox.showerror("输入错误", f"无效输入：'{self.entries[i][j].get()}'。请输入1到9之间的整数。")
                    return

        # 如果全部正确
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        messagebox.showinfo("成功通关！", f"恭喜你完成数独！\n用时：{int(elapsed_time)}秒")
        self.record_score(elapsed_time)  # 记录成绩

    def record_score(self, elapsed_time):
        """将游戏成绩写入文件。"""
        with open("sudoku_scores.txt", "a") as file:
            file.write(f"难度：{self.difficulty}, 时间：{int(elapsed_time)}秒\n")
        messagebox.showinfo("成绩记录", "成绩已被记录！")

# 运行游戏
if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
