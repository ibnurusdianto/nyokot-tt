import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.ttk import *
import os
import subprocess
import threading
import requests
import re
from datetime import datetime
import time

class TikTokDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Nyokot TT")
        master.configure(bg='#F0F0F0')
        master.geometry("700x400")

        self.label = tk.Label(master, text="Masukkan URL TikTok : ", font=("Helvetica", 12), bg='#F0F0F0')
        self.label.pack(pady=10)

        self.url_entry = tk.Entry(master, width=50, font=("Helvetica", 12))
        self.url_entry.pack(pady=10)

        self.browse_button = tk.Button(master, text="Pilih file .txt", command=self.browse_file, font=("Helvetica", 12), bg='#4CAF50', fg='white', activebackground='#3E8E41')
        self.browse_button.pack(pady=10)

        self.download_button = tk.Button(master, text="Download", command=self.download_video, font=("Helvetica", 12), bg='#4CAF50', fg='white', activebackground='#3E8E41')
        self.download_button.pack(pady=10)

        self.quit_button = tk.Button(master, text="Keluar", command=master.quit, font=("Helvetica", 12), bg='#F44336', fg='white', activebackground='#B71C1C')
        self.quit_button.pack(pady=10)

        self.progress_bar = tk.ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.note_label = tk.Label(master, text="Note: untuk versi file .txt harap masukin link nya tidak whitespace 2x, 1x saja!", font=("Helvetica", 10), bg='#F0F0F0')
        self.note_label.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, file_path)
        if file_path != "":
            messagebox.showinfo("Info", f"Anda telah memilih file {os.path.basename(file_path)}")

    def download_video(self):
        url = self.url_entry.get()
        if url == "":
            messagebox.showerror("Error", "Anda belum memasukkan link URL! Harap masukkan terlebih dahulu.")
        elif url.endswith(".txt"):
            if os.path.isfile(url):
                with open(url, 'r') as file:
                    urls = file.readlines()
                self.progress_bar["maximum"] = len(urls)
                self.progress_bar["value"] = 0
                for i, tiktok_url in enumerate(urls):
                    self.download_video_by_url(tiktok_url.strip())
                    self.progress_bar["value"] = i + 1
                messagebox.showinfo("Info", "Download selesai, terimakasih sudah menggunakan alat ini.")
            else:
                messagebox.showerror("Error", "File tidak ditemukan.")
        else:
            self.progress_bar["maximum"] = 1
            self.progress_bar["value"] = 0
            self.download_video_by_url(url)
            self.progress_bar["value"] = 1
            messagebox.showinfo("Info", "Download selesai, terimakasih sudah menggunakan alat ini.")

    def download_video_by_url(self, url):
        try:
            api_endpoint = 'https://www.tikwm.com/api/'
            params = {
                'url': url,
                'hd': 1
            }
            response = requests.get(api_endpoint, params=params)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['code'] == 0:
                    username = re.search(r'@(\w+)', url).group(1)
                    video_id = re.search(r'/video/(\d+)', url).group(1)
                    date_of_publish = datetime.now().strftime('%Y%m%d')
                    if not os.path.exists(username):
                        os.makedirs(username)
                    filename = os.path.join(username, f"{username}_{video_id}.mp4")
                    if not os.path.exists(filename):
                        video_url_without_watermark = response_data['data']['play']
                        video_data = requests.get(video_url_without_watermark).content
                        with open(filename, 'wb') as video_file:
                            video_file.write(video_data)
                        print(f"Video berhasil di download dan disimpan di : {filename}")
                    else:
                        print(f"Video sudah pernah di download sebelumnya : {filename}")
                else:
                    print(f"Error: {response_data['msg']}")
            else:
                print("Error")
        except:
            print("Error")

root = tk.Tk()
gui = TikTokDownloaderGUI(root)
root.mainloop()