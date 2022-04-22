import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
class main_window():
    def __init__(self, process_callback):
        self.root = tk.Tk()
        self.root.geometry("720x400")  # Size of the window
        self.root.title('TP1_traitement dimages')

        self.input = str(os.path.abspath(os.curdir))
        self.process_callback = process_callback
        self.img_ref = ""
        self.img_cmp = ""
        self.my_font1 = ('times', 18, 'bold')

        self.button1 = tk.Button(self.root, text='Charger image de référence', width=30, command=self.upload_image_ref)
        self.button1.grid(row=2, column=0)

        self.button2 = tk.Button(self.root, text="Charger image à comparer", width=30, command=self.upload_image_compare)
        self.button2.grid(row=3, column=0)

        self.button3 = tk.Button(self.root, text='Appliquer détection', width=30, command= self.Apply)
        self.button3.grid(row=4, column=0)

        score_label_title = tk.Label(self.root, text="Pourcentage d'encombrement:")
        score_label_title.place(x=450, y=360)
        self.textScore = tk.StringVar()
        self.textScore.set("0%")
        score_label = tk.Label(self.root, textvariable=self.textScore)
        score_label.place(x=650, y=360)

        self.show_steps = False
        self.checkbox = ttk.Checkbutton(self.root, text="Afficher les étapes",
                        command=self.check_changed, onvalue=True, offvalue=False)
        self.checkbox.grid(row=6, column=0)

        self.root.mainloop()  # Keep the window open

    ### Apply button handle ###
    def Apply(self):
        img_out, score = self.process_callback(self.img_ref, self.img_cmp, self.show_steps)
        self.textScore.set(str(score)+"%")
        img_out = Image.fromarray(img_out)
        self.place_on_window(img_out, 2)

    ### UI handle ###
    def check_changed(self):
        self.show_steps = not self.show_steps
        print("Afficher les etapes: "+ str(self.show_steps))

    ### Image selection ####
    def upload_img(self):
        f_types = [('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(initialdir=input, filetypes=f_types)
        img_opened = Image.open(filename)
        return filename, img_opened

    def place_on_window(self, img_to_place, col):
        img_resized = img_to_place.resize((350, 270))  # new width & height
        img_tk = ImageTk.PhotoImage(img_resized)
        label = tk.Label(self.root, image=img_tk)
        label.image = img_tk
        label.grid(row=5, column=col)

    def upload_image_ref(self):
        self.img_ref, im_opened = self.upload_img()
        self.place_on_window(im_opened, 0)

    def upload_image_compare(self):
        self.img_cmp, im_opened = self.upload_img()
        self.place_on_window(im_opened, 2)
