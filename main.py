import os
import requests
import sys
import darkdetect
import wget
import ctypes
import subprocess
import json
import tkinter
from tkinter import StringVar
from tkinter import ttk
from tkinter import messagebox
# from PIL import Image, ImageTk

import sv_ttk

baseDir = os.path.dirname(os.path.realpath(sys.argv[0]))

def dark_title_bar(window):
	"使标题栏变黑"
	window.update()
	DWMWA_USE_IMMERSIVE_DARK_MODE = 20
	set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
	get_parent = ctypes.windll.user32.GetParent
	hwnd = get_parent(window.winfo_id())
	rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
	value = 2
	value = ctypes.c_int(value)
	set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))
	window.update()


def centerWindow(window):
    "窗口居中"
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def main():
    # global icon

    # 检测IP
    ip = requests.get('https://4.ipw.cn').text.strip()
    # os.system(f'curl -o %temp%\country_code https://ipapi.co/{ip}/country/')
    wget.download(f'https://ipapi.co/{ip}/country/', os.getenv("temp") + "\country_code")
    location = open(os.getenv("temp") + "\country_code", encoding="utf-8")
    countryCode = location.read()
    print(countryCode)
    location.close()
    os.remove(os.getenv("temp") + "\country_code")
    noytm = ["CN", "MO", "KP", "RU"]
    if countryCode in noytm:
        messagebox.showerror(title=None, message="检测到你的IP似乎无法使用YouTube Music")
        sys.exit()
    
    checking.destroy()

    # 获取URL

    def saveSettings():
        "保存设置"

        print(outputstr.get())
        print(optstr.get())

        settingsOps = {
            "OutputPath" : outputstr.get(),
            "Options" : optstr.get()
        }

        settingsJson = json.dumps(settingsOps)
        #保存
        config = os.getenv("userprofile") + "\AppData\Roaming\spotDL"
        if not os.path.exists(config):
            os.makedirs(config)
        f = open(config + "\config.json", "w", encoding="utf-8")
        f.write(settingsJson)

    def settings():
        "设置"

        settingsButton.pack_forget()

        exitButton.pack(side="top", anchor="ne", padx=10, pady=10)

        saveSet.pack(side="bottom", anchor="se", padx=10, pady=10)

        outputTitle.pack()

        outputEntry.pack(pady=10)

        optTitle.pack()

        optEntry.pack(pady=10)
        

    def download():
        "下载"
        res = urlstr.get()
        print(res)
        
        if "open.spotify.com/album/" in res or "open.spotify.com/track/" in res or "music.youtube.com/playlist?list=" in res or "music.youtube.com/watch?v=" in res:
            entry.destroy()
            tips.destroy()

            exitButton.pack_forget()
            outputTitle.pack_forget()
            outputEntry.pack_forget()
            saveSet.pack_forget()
            optTitle.pack_forget()
            optEntry.pack_forget()
            
            # 设置按钮
            settingsButton.pack(side="top", anchor="ne", padx=10, pady=10)

            

            
        
        else:
            messagebox.showwarning(title=None, message='请输入正确的单曲或专辑链接（"open.spotify.com/*" 或 "music.youtube.com/*"）')


    entry = ttk.Frame(root)
    urlstr = StringVar()
    url = ttk.Entry(entry, width=56, textvariable=urlstr)
    nxt = ttk.Button(entry, text="→", command=download)
    entry.grid(pady=72)
    url.grid(row=0, column=0, padx=17, pady=0, sticky="nesw")
    nxt.grid(row=0, column=1, pady=0, sticky="nesw")

    # icon = ImageTk.PhotoImage(Image.open("./res/icons.png"))
    # iconLabel = ttk.Label(entry, image=icon)
    # iconLabel.grid(row=1, column=0, padx=30, pady=30, sticky="nesw")

    tips = ttk.Label(root, text="支持Spotify、YouTube Music中的单曲、专辑")
    tips.grid(row=1, column=0, padx=105, sticky="nesw")

    # 设置
    settingsButton = ttk.Button(root, text="⚙️", command=settings)
    exitButton = ttk.Button(root, text="🏠", command=download)
    outputTitle = ttk.Label(root, text="输出路径")
    outputstr = StringVar()
    outputEntry = ttk.Entry(root, width=40, textvariable=outputstr)
    saveSet = ttk.Button(root, text="保存", command=saveSettings)
    optTitle = ttk.Label(root, text="自定义参数")
    optstr = StringVar()
    optEntry = ttk.Entry(root, width=40, textvariable=optstr)


root = tkinter.Tk()

root.title("spotDL")
root.geometry("500x270")
centerWindow(root)
root.resizable(False, False)

checking = ttk.Label(root, text="正在检测环境…")
checking.pack(ipady=150)




# This is where the magic happens
if darkdetect.isDark():
    sv_ttk.use_dark_theme()
    dark_title_bar(root)
else:
    sv_ttk.use_light_theme()

main()

root.mainloop()