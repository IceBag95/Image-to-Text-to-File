import pandas as pd
from PIL import Image
import pytesseract
import tkinter as tk
import customtkinter as ctk
import docx
import os
from pathlib import Path
from tkinterdnd2 import *


# IF NEEDED
#file: customtkinter>windows>ctk_tk.py

#Then do these changes in the ctk_tk.py file of customtkinter library.

#Add this new import: from tkinterdnd2 import *
#Replace (Ctrl+H) this term: tkinter.Tk with TkinterDnD.Tk.
#Save the file.
#Done!



# CLASSES
class CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# FUNCTIONS

def on_drop(event):
    event.widget.delete(0, tk.END) #σβήνει το περιεχόμενο του entry
    file_path = event.data
    file_path ='"' +file_path[1:len(file_path)-1] + '"'
    file_path =  Path(file_path)
    event.widget.insert(0, file_path) #γράφει το περιεχόμενο του entry
    print("File path:", file_path)


def correct_path():
    path = entry.get()
    path = path.strip()

    if len(path)>0:
        if path[0] == '"':
            path = path[1:len(path)-1]

        return path

    else:
        return ''


def turn_into_word(path):
    print('word\n', path)
    data_str = pytesseract.image_to_string(Image.open(path), lang='eng+ell')
    datalist.append(data_str)
    print(datalist)
    countLabel.configure(text=f'Text form images extracted: {len(datalist)}')
    text_area.configure(state='normal')
    text_area.delete(0.0,'end')
    text_area.insert(0.0, data_str)
    text_area.configure(state='disabled')





def turn_into_excel(path):
    pass


def showtime():

    result_label.configure(text='')

    path = correct_path()

    if os.path.exists(path) and (path.endswith('.png') or path.endswith('.jpg')):

        if int(radio_var.get()) == 1:
            turn_into_word(path)
        else:
            turn_into_excel(path)

    else:
        print('Path does not exist')
        result_label.configure(text='WARNING: Not a correct path or not supported image type',
                               text_color='#ff0000')


def make_file():
    pass


# INITIATIONS
datalist = []




# WINDOW SPECS
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'




root = CTk()
root.geometry('700x800')


input_label = ctk.CTkLabel(root, text='Please enter image path or drag and drop file:\n(Supports .png and .jpg files)')
input_label.pack()


entry = ctk.CTkEntry(root, width=500)
entry.pack()

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', on_drop)



radio_var = ctk.StringVar()
radio1 = ctk.CTkRadioButton(root,text='Word File',
                            variable=radio_var,
                            value=1)
radio1.pack()
radio2 = ctk.CTkRadioButton(root,text='Excel File (currently on development)',
                            variable=radio_var,
                            value=2,
                            state='disabled')
radio2.pack()

radio_var.set('radiobuttons')
radio1.select()

text_label = ctk.CTkLabel(root,
                          text='Extracted Text',
                          padx=20,
                          pady=10)
text_label.pack()


text_area = ctk.CTkTextbox(root,
                           pady=10,
                           padx=10,
                           width=500,
                           height=500,
                           state='disabled')
text_area.pack()




result_label = ctk.CTkLabel(root, text='')
result_label.pack()

go_button = ctk.CTkButton(root, text='GO!', command=showtime)
go_button.pack()

countLabel = ctk.CTkLabel(root, text='Text form images extracted: 0')
countLabel.pack()

make_doc = ctk.CTkButton(root, text='Stop and Create new Word Document',
                         state='disabled',command=make_file)
make_doc.pack()


root.mainloop()
