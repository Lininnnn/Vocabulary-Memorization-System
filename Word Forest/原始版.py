import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# 数据文件
USER_DATA_FILE = "users.json"
WORDS_DATA_FILE = "words.json"

# 用户数据
users_data = {}
# 单词本数据
words_data = {}


def load_data():
    """加载用户数据和单词数据"""
    global users_data, words_data
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            users_data = json.load(file)
    if os.path.exists(WORDS_DATA_FILE):
        with open(WORDS_DATA_FILE, "r", encoding="utf-8") as file:
            words_data = json.load(file)


def save_data():
    """保存数据"""
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users_data, file, indent=4, ensure_ascii=False)
    with open(WORDS_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(words_data, file, indent=4, ensure_ascii=False)


def validate_input(user_input, input_type="text"):
    """简单的输入验证"""
    if input_type == "text" and len(user_input.strip()) == 0:
        return False
    if input_type == "number" and not user_input.isdigit():
        return False
    return True


def register_user(username, password):
    """注册新用户"""
    if username in users_data:
        return False
    users_data[username] = {
        "password": password,
        "total_score": 0,
        "correct_count": 0,
        "wrong_count": 0,
        "study_days": 0,
        "wrong_words": []
    }
    save_data()
    return True


def login_user(username, password):
    """用户登录验证"""
    if username in users_data and users_data[username]["password"] == password:
        return True
    return False


def add_word(word, part_of_speech, meaning):
    """增加单词"""
    words_data[word] = {
        "part_of_speech": part_of_speech,
        "meaning": meaning,
        "frequency": 0,
        "correct_rate": 0
    }
    save_data()


def modify_word(word, part_of_speech=None, meaning=None):
    """修改单词"""
    if word in words_data:
        if part_of_speech:
            words_data[word]["part_of_speech"] = part_of_speech
        if meaning:
            words_data[word]["meaning"] = meaning
        save_data()


def delete_word(word):
    """删除单词"""
    if word in words_data:
        del words_data[word]
        save_data()

def recite_mode(username):
    """背诵模式：用户浏览单词和释义"""

    def show_word():
        """更新当前单词显示"""
        word = word_list[current_word_index]
        word_info = words_data[word]
        word_label.config(text=f"单词: {word}")
        meaning_label.config(text=f"含义: {word_info['meaning']}")
        progress_label.config(text=f"数量: {current_word_index + 1}/{len(word_list)}")

    def next_word():
        """显示下一个单词"""
        nonlocal current_word_index
        current_word_index = (current_word_index + 1) % len(word_list)
        show_word()

    def previous_word():
        """显示上一个单词"""
        nonlocal current_word_index
        current_word_index = (current_word_index - 1) % len(word_list)
        show_word()

    word_list = list(words_data.keys())
    current_word_index = 0

    # 创建主界面窗口
    root = tk.Tk()
    root.geometry("600x400")
    root.title("背诵模式")

    word_label = tk.Label(root, text="Word:", font=("Arial", 18))
    word_label.pack(pady=10)

    meaning_label = tk.Label(root, text="Meaning:", font=("Arial", 14))
    meaning_label.pack(pady=10)

    prev_button = tk.Button(root, text="上一词", font=("Arial", 14), command=previous_word)
    prev_button.pack(side=tk.LEFT, padx=20, pady=10)

    next_button = tk.Button(root, text="下一词", font=("Arial", 14), command=next_word)
    next_button.pack(side=tk.RIGHT, padx=20, pady=10)

    progress_label = tk.Label(root, text="Progress: 0/0", font=("Arial", 12))
    progress_label.pack(pady=10)

    show_word()
    root.mainloop()
def spell_mode(username):
    """拼写模式：用户根据释义输入单词"""

    def next_word():
        """显示下一个单词"""
        nonlocal current_word_index
        if current_word_index < len(word_list):
            word = word_list[current_word_index]
            word_info = words_data[word]
            word_label.config(text=f"词性: {word_info['part_of_speech']}")
            meaning_label.config(text=f"含义: {word_info['meaning']}")
            answer_entry.delete(0, tk.END)
            progress_label.config(text=f"数量: {current_word_index + 1}/{len(word_list)}")
            current_word_index += 1
        else:

            messagebox.showinfo("学习完成", f"拼写模式结束！\n正确数量：{correct_count}\n错误数量：{wrong_count}")
            root.quit()  # 退出主界面
            root.destroy()  # 销毁窗口并退出

    def check_answer():
        """检查答案"""
        nonlocal correct_count, wrong_count
        user_answer = answer_entry.get().strip()
        current_word = word_list[current_word_index - 1]
        if user_answer.lower() == current_word.lower():
            result_label.config(text="Correct!", fg="green")
            correct_count += 1
        else:
            result_label.config(text=f"Wrong! Correct: {current_word}", fg="red")
            wrong_count += 1
            # 保存错误单词到错题本
            users_data[username]["wrong_words"].append(current_word)
            save_data()  # 保存数据到文件或数据库
        next_word()

    word_list = list(words_data.keys())
    random.shuffle(word_list)
    current_word_index = 0
    correct_count = 0
    wrong_count = 0

    # 创建主界面窗口
    root = tk.Tk()
    root.geometry("600x400")
    root.title("拼写模式")

    meaning_label = tk.Label(root, text="Meaning:", font=("Arial", 14))
    meaning_label.pack(pady=10)
    word_label = tk.Label(root, text="Word:", font=("Arial", 18))
    word_label.pack(pady=10)
    answer_label = tk.Label(root, text="Your answer:", font=("Arial", 14))
    answer_label.pack(pady=5)

    answer_entry = tk.Entry(root, font=("Arial", 14), width=20)
    answer_entry.pack(pady=5)

    check_button = tk.Button(root, text="Check Answer", font=("Arial", 14), command=check_answer)
    check_button.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.pack(pady=5)

    progress_label = tk.Label(root, text="Progress: 0/0", font=("Arial", 12))
    progress_label.pack(pady=5)

    next_word()
    root.mainloop()
def choose_study_mode(username):
    """选择学习模式界面"""

    def start_study(mode):
        """启动对应的学习模式"""
        root.quit()
        if mode == "recite":
            recite_mode(username)
        elif mode == "spell":
            spell_mode(username)

    root = tk.Tk()
    root.geometry("400x200")
    root.title("选择学习模式")

    recite_button = tk.Button(root, text="背诵模式", font=("Arial", 14), width=20,
                              command=lambda: start_study("recite"))
    recite_button.pack(pady=20)

    spell_button = tk.Button(root, text="拼写模式", font=("Arial", 14), width=20, command=lambda: start_study("spell"))
    spell_button.pack(pady=20)

    root.mainloop()





def review_wrong_words(username):
    """复习错题本（图形界面版）"""
    wrong_words = users_data[username]["wrong_words"]

    if not wrong_words:
        messagebox.showinfo("没有错题", "没有错题可复习！")
        return

    current_word_index = 0

    def show_next_word():
        """显示下一个错题"""
        nonlocal current_word_index
        if current_word_index < len(wrong_words):
            word = wrong_words[current_word_index]
            word_info = words_data[word]
            word_label.config(text=f"单词: {word}")
            meaning_label.config(text=f"含义: {word_info['meaning']}")
            current_word_index += 1
        else:
            # 复习完成后删除错题单词
            users_data[username]["wrong_words"] = []
            save_data()  # 确保错题本数据被保存
            messagebox.showinfo("复习完成", "恭喜！你已复习完所有错题！")
            root.quit()  # 关闭窗口

    def show_prev_word():
        """显示上一个错题"""
        nonlocal current_word_index
        if current_word_index > 0:
            current_word_index -= 1
            word = wrong_words[current_word_index]
            word_info = words_data[word]
            word_label.config(text=f"单词: {word}")
            meaning_label.config(text=f"含义: {word_info['meaning']}")

    # 创建复习错题的窗口
    root = tk.Tk()
    root.geometry("600x400")
    root.title("错题本复习")

    # 显示当前错题的单词和释义
    word_label = tk.Label(root, text="单词:", font=("Arial", 18))
    word_label.pack(pady=10)

    meaning_label = tk.Label(root, text="含义:", font=("Arial", 14))
    meaning_label.pack(pady=10)

    # 显示复习进度
    progress_label = tk.Label(root, text=f"数量: {current_word_index}/{len(wrong_words)}", font=("Arial", 12))
    progress_label.pack(pady=5)

    # 前一个和下一个按钮
    prev_button = tk.Button(root, text="上一题", font=("Arial", 14), command=show_prev_word)
    prev_button.pack(side=tk.LEFT, padx=20, pady=20)

    next_button = tk.Button(root, text="下一题", font=("Arial", 14), command=lambda: [show_next_word(),
                                                                                      progress_label.config(
                                                                                          text=f"数量: {current_word_index}/{len(wrong_words)}")])
    next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    # 显示第一个错题
    show_next_word()

    root.mainloop()

def clock_in(username):
    """打卡并弹出成功提示框"""
    # 更新打卡天数
    users_data[username]["study_days"] += 1

    # 保存数据
    save_data()

    # 弹出提示框，提示用户打卡成功
    messagebox.showinfo("打卡成功", f"{username}，打卡成功！已累计学习 {users_data[username]['study_days']} 天。")


def create_main_window():
    """创建主窗口"""
    root = tk.Tk()
    root.geometry("800x600")
    root.title("单词学习系统")

    def show_login_screen():
        """显示登录界面"""
        root.geometry("400x300")  # 登录页面的尺寸

        login_frame = tk.Frame(root)
        login_frame.pack(expand=True)  # 让登录框在窗口中居中

        # 创建标签和输入框
        tk.Label(login_frame, text="用户名:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(login_frame, text="密码:").grid(row=1, column=0, padx=10, pady=5, sticky="w")

        username_entry = tk.Entry(login_frame)
        password_entry = tk.Entry(login_frame, show="*")

        username_entry.grid(row=0, column=1, padx=10, pady=5)
        password_entry.grid(row=1, column=1, padx=10, pady=5)


        def login_action():
            username = username_entry.get()
            password = password_entry.get()

            if not validate_input(username) or not validate_input(password):
                messagebox.showerror("错误", "请输入有效的用户名和密码")
                return

            if login_user(username, password):
                messagebox.showinfo("成功", "登录成功")
                login_frame.pack_forget()
                show_main_screen(username)
            else:
                messagebox.showerror("错误", "用户名或密码错误")

        def register_action():
            username = username_entry.get()
            password = password_entry.get()

            if not validate_input(username) or not validate_input(password):
                messagebox.showerror("错误", "请输入有效的用户名和密码")
                return

            if register_user(username, password):
                messagebox.showinfo("成功", "注册成功")
                login_frame.pack_forget()
                show_main_screen(username)
            else:
                messagebox.showerror("错误", "用户名已存在")

        login_button = tk.Button(login_frame, text="登录", command=login_action, width=8, height=1)
        register_button = tk.Button(login_frame, text="注册", command=register_action, width=8, height=1)
        # 将按钮放在同一行，并且水平居中
        login_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")  # "登录" 按钮靠右
        register_button.grid(row=2, column=1, padx=3, pady=10, sticky="e")  # "注册" 按钮靠左

        # 控件居中并工整
        login_frame.grid_columnconfigure(0, weight=1)  # 列0占用所有可用空间
        login_frame.grid_columnconfigure(1, weight=1)  # 列1也占用空间，保证对齐
        login_frame.grid_rowconfigure(0, weight=1)  # 行0、1和2也可以扩展，使控件居中
        login_frame.grid_rowconfigure(1, weight=1)
        login_frame.grid_rowconfigure(2, weight=1)

        # 使得窗口在屏幕中居中
        root.update()
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        root.geometry(f'{width}x{height}+{position_left}+{position_top}')  # 设置位置

    def show_main_screen(username):
        """显示主界面"""
        root.geometry("700x500")  # 主页面的尺寸
        main_frame = tk.Frame(root)
        main_frame.pack(padx=20, pady=20)  # 给整个框架添加一些外边距

        # 显示欢迎信息
        welcome_label = tk.Label(main_frame, text=f"欢迎, {username}", font=("Arial", 16))
        welcome_label.pack(pady=(1,1))  # 上下间距

        # 获取用户的成绩数据
        if username in users_data:
            user_info = users_data[username]
            total_score = user_info["total_score"]
            correct_count = user_info["correct_count"]
            wrong_count = user_info["wrong_count"]
            study_days = user_info["study_days"]


            # 显示用户成绩信息
            info_text = (
                f"总分: {total_score} | "
                f"正确回答数: {correct_count} | "
                f"错误回答数: {wrong_count} | "
                f"学习天数: {study_days} 天"
            )

            # 显示成绩信息的 Label
            info_label = tk.Label(main_frame, text=info_text, font=("Arial", 12), justify="center")
            info_label.pack(pady=10)

        # 按钮设置
        button_config = {
            "width": 20,  # 设置按钮的宽度
            "height": 1,  # 设置按钮的高度
            "padx": 10,  # 按钮水平间距
            "pady": 10  # 按钮垂直间距
        }

        # 使用 grid 布局管理器来排列按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)  # 按钮区域的垂直间距

        # 开始背单词按钮
        start_button = tk.Button(button_frame, text="开始背单词", command=lambda: choose_study_mode(username), **button_config)
        start_button.grid(row=0, column=0, padx=10, pady=1, sticky="ew")

        # 错题复习按钮
        review_button = tk.Button(button_frame, text="错题复习", command=lambda: review_wrong_words(username),
                                  **button_config)
        review_button.grid(row=1, column=0, padx=10, pady=1, sticky="ew")

        # 打卡按钮
        clock_in_button = tk.Button(button_frame, text="打卡", command=lambda: clock_in(username), **button_config)
        clock_in_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # 管理单词本按钮
        manage_button = tk.Button(button_frame, text="管理单词本", command=show_word_management_screen, **button_config)
        manage_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # 退出按钮
        exit_button = tk.Button(button_frame, text="退出", command=root.quit, **button_config)
        exit_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # 调整窗口居中
        root.update()
        width = root.winfo_width()
        height = root.winfo_height()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)

        root.geometry(f'{width}x{height}+{position_left}+{position_top}')  # 设置位置


    def show_word_management_screen():
        """显示单词本管理界面"""
        management_frame = tk.Toplevel(root)
        management_frame.title("单词本管理")

        tk.Label(management_frame, text="单词:").grid(row=0, column=0)
        tk.Label(management_frame, text="词性:").grid(row=1, column=0)
        tk.Label(management_frame, text="释义:").grid(row=2, column=0)

        word_entry = tk.Entry(management_frame)
        pos_entry = tk.Entry(management_frame)
        meaning_entry = tk.Entry(management_frame)

        word_entry.grid(row=0, column=1)
        pos_entry.grid(row=1, column=1)
        meaning_entry.grid(row=2, column=1)

        def add_word_action():
            """添加单词"""
            word = word_entry.get()
            pos = pos_entry.get()
            meaning = meaning_entry.get()
            if validate_input(word) and validate_input(pos) and validate_input(meaning):
                if word in words_data:
                    messagebox.showerror("错误", "单词已存在")
                else:
                    add_word(word, pos, meaning)
                    messagebox.showinfo("成功", "单词已添加")
                    refresh_word_list()  # 添加成功后刷新列表
            else:
                messagebox.showerror("错误", "请输入有效的单词信息")

        def modify_word_action():
            """修改选中的单词"""
            word = word_entry.get()
            pos = pos_entry.get()
            meaning = meaning_entry.get()
            if validate_input(word):
                if word in words_data:
                    modify_word(word, part_of_speech=pos, meaning=meaning)
                    messagebox.showinfo("成功", "单词已修改")
                    refresh_word_list()  # 修改成功后刷新列表
                else:
                    messagebox.showerror("错误", "单词不存在")
            else:
                messagebox.showerror("错误", "请输入有效的单词信息")

        def delete_word_action():
            """删除单词"""
            word = word_entry.get()
            if validate_input(word):
                if word in words_data:
                    delete_word(word)
                    messagebox.showinfo("成功", "单词已删除")
                    refresh_word_list()  # 删除后刷新列表
                else:
                    messagebox.showerror("错误", "单词不存在")
            else:
                messagebox.showerror("错误", "请输入有效的单词")

        def refresh_word_list():
            """刷新单词列表"""
            word_listbox.delete(0, tk.END)
            for word, info in words_data.items():
                word_listbox.insert(tk.END, f"{word} ({info['part_of_speech']}): {info['meaning']}")

        def on_word_select(event):
            """选择单词时自动填充到输入框"""
            selected_word = word_listbox.get(word_listbox.curselection())
            word = selected_word.split(' ')[0]  # 获取单词
            pos = selected_word.split('(')[1].split(')')[0]  # 获取词性
            meaning = selected_word.split(': ')[1]  # 获取释义

            word_entry.delete(0, tk.END)
            pos_entry.delete(0, tk.END)
            meaning_entry.delete(0, tk.END)

            word_entry.insert(0, word)
            pos_entry.insert(0, pos)
            meaning_entry.insert(0, meaning)

        # 单词列表显示
        word_listbox = tk.Listbox(management_frame, width=50, height=10)
        word_listbox.grid(row=4, column=0, columnspan=3)
        word_listbox.bind("<Double-1>", on_word_select)  # 双击选择单词填充

        # 刷新按钮
        refresh_button = tk.Button(management_frame, text="刷新单词列表", command=refresh_word_list)
        refresh_button.grid(row=5, column=1)

        # 操作按钮
        tk.Button(management_frame, text="添加单词", command=add_word_action).grid(row=3, column=0)
        tk.Button(management_frame, text="修改单词", command=modify_word_action).grid(row=3, column=1)
        tk.Button(management_frame, text="删除单词", command=delete_word_action).grid(row=3, column=2)

        # 初次加载单词列表
        refresh_word_list()

    show_login_screen()
    root.mainloop()


if __name__ == "__main__":
    load_data()
    create_main_window()
