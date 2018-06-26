import Tkinter as tk
import random
import threading
import tkMessageBox
import tkFileDialog

from got_fetcher import get_seasons, get_episode_data
from colors_got import all_colors


class GOT_Download_GUI:
    def __init__(self, master):
        self.master = master
        master.title("GOT downloader")
        master.configure(background='aquamarine')

        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        master.config(menu=menu_bar)

        self.download_button = tk.Button(master, text="download data", command=self.get_got_data)
        self.logo = tk.PhotoImage(file="got.gif")
        self.download_button.config(image=self.logo, activebackground="black", bg="black", bd=0)
        self.download_button.pack()

        self.results_text = tk.Text(root, state='disabled', height=12, width=50)
        self.results_text.pack()

        self.cancel_button = tk.Button(master, text="Cancel download", command=self.cancel_download)
        self.cancel_button.config(state=tk.DISABLED)
        self.cancel_button.pack()

        self.canvas_width = 360  # 8 * 40
        self.canvas_height = 200
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.stop_thread = False

    def save_results(self):
        f = tkFileDialog.asksaveasfile(mode='w', initialfile="got_download_data", defaultextension=".txt")
        if f is None:
            return
        text_to_write = str(self.results_text.get(1.0, tk.END))
        f.write(text_to_write)
        f.close()

    def about(self):
        text = "A GUI app to web scrape wikipedia for Game of Thrones view stats"
        tkMessageBox.showinfo("About", text)

    def draw_lines(self, seasons):
        size = 40

        random_colors = random.sample(all_colors, len(seasons))

        for index, s in enumerate(seasons, start=1):
            self.canvas.create_rectangle(2 + (size * index), self.canvas_height - round(s.season_total),
                                         40 + (size * index), 200, fill=random_colors[index - 1])

            self.canvas.create_text(20 + (size * index), 10, fill="darkblue", font="Times 10 italic bold",
                                    text="S{}".format(index))

        self.canvas.create_text(100, 50, fill="darkblue", font="Times 10 italic bold",
                                text="Total views {}".format(sum(s.season_total for s in seasons)))

    def cancel_download(self):
        self.stop_thread = True

    def _set_allow_download_state(self):
        self.download_button.config(state="normal")
        self.cancel_button.config(state=tk.DISABLED)

    def _set_allow_cancel_state(self):
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state="normal")

    def write_results_text(self, text):
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, text)
        self.results_text.configure(state='disabled')

    def get_got_data(self):
        self._set_allow_cancel_state()
        # clear gui
        self.write_results_text("")
        self.canvas.delete("all")

        def callback():
            seasons = get_seasons()
            for season in seasons[:-1]:
                get_episode_data(season)
                if self.stop_thread:
                    break

            text = ""
            running_total = 0
            for s in seasons:
                if self.stop_thread:
                    break
                text += s.name + " " + str(s.season_total) + "\n"
                running_total += s.season_total

            if self.stop_thread:
                self.write_results_text("Download Aborted")
                self.stop_thread = False
            else:
                text += "Overall total: " + str(running_total)
                self.draw_lines(seasons)
                self.write_results_text(text)

            self._set_allow_download_state()

        thread = threading.Thread(target=callback)
        thread.daemon = True
        thread.start()


root = tk.Tk()
my_gui = GOT_Download_GUI(root)
root.mainloop()
