import Tkinter as tk
import random
import threading

from got_fetcher import get_seasons, get_episode_data
from colors_got import all_colors


class GOT_Download_GUI:
    def __init__(self, master):
        self.master = master
        master.title("GOT downloader")
        self.logo = tk.PhotoImage(file="got.gif")
        self.label = tk.Label(master, image=self.logo)
        self.label.pack()

        self.download_button = tk.Button(master, text="download data", command=self.get_got_data)
        self.download_button.pack()

        self.results_text = tk.Text(root, height=12, width=50)
        self.results_text.pack()

        self.cancel_button = tk.Button(master, text="Cancel download", command=self.cancel_download)
        self.cancel_button.config(state=tk.DISABLED)
        self.cancel_button.pack()

        self.canvas_width = 360  # 8 * 40
        self.canvas_height = 200
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.stop_thread = False

    def draw_lines(self, seasons):
        size = 40

        random_colors = random.sample(all_colors, len(seasons))

        for index, s in enumerate(seasons, start=1):
            self.canvas.create_rectangle(2 + (size * index), self.canvas_height - round(s.season_total),
                                         40 + (size * index), 200, fill=random_colors[index - 1])

            self.canvas.create_text(20 + (size * index), 10, fill="darkblue", font="Times 10 italic bold",
                                    text="S{}".format(index))

    def cancel_download(self):
        self.stop_thread = True

    def _set_allow_download_state(self):
        self.download_button.config(state="normal")
        self.cancel_button.config(state=tk.DISABLED)

    def _set_allow_cancel_state(self):
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state="normal")

    def get_got_data(self):

        self._set_allow_cancel_state()
        # clear gui
        self.results_text.delete(1.0, tk.END)
        self.canvas.delete("all")

        def callback():
            cancelled = False
            seasons = get_seasons()
            for season in seasons[:-1]:
                get_episode_data(season)
                if self.stop_thread:
                    cancelled = True
                    break

            text = ""
            running_total = 0
            for s in seasons:
                if self.stop_thread:
                    cancelled = True
                    break
                text += s.name + " " + str(s.season_total) + "\n"
                running_total += s.season_total

            if cancelled:
                self.results_text.insert(tk.END, "Download Aborted")
            else:
                text += "Overall total: " + str(running_total)
                self.draw_lines(seasons)
                self.results_text.insert(tk.END, text)

            self._set_allow_download_state()

        thread = threading.Thread(target=callback)
        thread.daemon = True
        thread.start()


root = tk.Tk()
my_gui = GOT_Download_GUI(root)
root.mainloop()
