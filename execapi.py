import os
import tkinter as tk
from tkinter import filedialog

def run_python_file():
    # 使用文件選擇對話框選擇Python檔案
    file_path = filedialog.askopenfilename(title="選擇Python檔案", filetypes=[("Python檔案", "*.py")])
    
    # 如果選擇了一個檔案，執行該檔案
    if file_path:
        os.system("python " + file_path)

# 創建Tkinter的根視窗
root = tk.Tk()

# 設置窗口標題
root.title("選擇Python腳本並執行")

# 設置窗口大小
root.geometry("400x200")

# 創建一個按鈕
button = tk.Button(root, text="選擇Python腳本並並執行", command=run_python_file)

# 將按鈕放置在窗口中央
button.pack(expand=True, fill="both")

# 進入主循環
root.mainloop()
