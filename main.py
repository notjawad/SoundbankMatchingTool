import glob
import struct
import shutil
import os
import threading

import tkinter as tk
import ttkbootstrap as ttk

from tkinter import filedialog, messagebox


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Soundbank Matching Tool")  # TODO: Change title
        self.geometry("500x500")
        self.resizable(False, False)

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Import", command=self.import_files)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)

        self.listbox1 = tk.Listbox(self)
        self.listbox1.pack(expand=True, fill="both", padx=10, pady=10)

        self.listbox2 = tk.Listbox(self)
        self.listbox2.pack(expand=True, fill="both", padx=10, pady=10)

        self.match_btn = ttk.Button(
            self,
            text="Extract",
            command=threading.Thread(target=self.extract, daemon=True).start,
            bootstyle="dark",
        ).pack(side="bottom", padx=10, pady=10)

        self.progress_text = tk.StringVar()
        self.progress_text.set("Not started")
        self.progress_label = ttk.Label(
            self, textvariable=self.progress_text, bootstyle="dark"
        )
        self.progress_label.pack(side="bottom", padx=10, pady=10)

        self.soundbank_files = []
        self.wem_files = []

        self.scrollbar1 = ttk.Scrollbar(
            self.listbox1, orient="vertical", bootstyle="dark-round"
        )
        self.scrollbar1.pack(side="right", fill="y")
        self.listbox1.config(yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.config(command=self.listbox1.yview)

        self.scrollbar2 = ttk.Scrollbar(
            self.listbox2, orient="vertical", bootstyle="dark-round"
        )
        self.scrollbar2.pack(side="right", fill="y")
        self.listbox2.config(yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.listbox2.yview)

    def import_files(self):
        soundbanks = tk.filedialog.askdirectory(title="Select soundbanks folder")
        if len(soundbanks) > 0:
            for file in glob.glob(f"{soundbanks}/*"):
                self.soundbank_files.append(file)

            for count, value in enumerate(self.soundbank_files):
                text = f"{count + 1}. {value.split('/')[-1]}"
                self.listbox1.insert("end", text)

        wems = tk.filedialog.askdirectory(title="Select wems folder")
        if len(wems) > 0:
            for file in glob.glob(f"{wems}/*"):
                self.wem_files.append(file)

            for count, value in enumerate(self.wem_files):
                text = f"{count + 1}. {value.split('/')[-1]}"
                self.listbox2.insert("end", text)

    def extract(self):
        self.progress_text.set("Extracting...")
        files_matched = 0
        files_left = len(self.wem_files)
        for soundbank in self.soundbank_files:
            with open(soundbank, "rb") as soundbank_file:
                data = soundbank_file.read()

            for i in range(len(data)):
                if data.startswith(b"RIFF", i):
                    file_size = struct.unpack("<I", data[i + 4 : i + 8])[0]

                    for wem in self.wem_files:
                        with open(wem, "rb") as f:
                            wem_header = f.read(8)

                            # format: 52 49 46 46 xx xx xx xx
                            hex_str = " ".join(["{:02x}".format(x) for x in wem_header])

                            hex_list = hex_str.split(" ")[-4:]
                            hex_str = "".join(hex_list)
                            wem_file_size = struct.unpack("<I", bytes.fromhex(hex_str))[
                                0
                            ]

                            if file_size == wem_file_size:
                                if not os.path.exists("matches"):
                                    os.makedirs("matches")

                                shutil.copy(wem, "matches")
                                soundbank_name = soundbank_file.name.split("\\")[
                                    -1
                                ].replace(".soundbank", "")
                                asset_name = os.path.basename(f.name)
                                if os.path.exists(
                                    f"matches/{soundbank_name}_{asset_name}"
                                ):
                                    pass
                                else:
                                    os.rename(
                                        f"matches/{os.path.basename(wem)}",
                                        f"matches/{soundbank_name}_{asset_name}",
                                    )

                                    print(
                                        f"Saved to matches/{soundbank_name}_{asset_name}"
                                    )

            files_matched += 1
            files_left -= 1
            self.progress_text.set(
                f"Matched {files_matched}/{len(self.soundbank_files)} soundbanks. {files_left} wem files left."
            )


if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except Exception as e:
        print(e)
