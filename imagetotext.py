import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk


API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

def display_image(filename):
    img=Image.open(filename)
    img=img.resize((300,300),Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image=img_tk

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def browse_file():
    filename=filedialog.askopenfilename(title="select an image File",
                                        filetypes=[('Image Files',"*.jpg *.png **.bmp")])
    if filename:
        display_image(filename)
        caption=query_image_caption(filename)
        if caption:
            result_label.config(text='Caption: '+caption)
        else:
            messagebox.showerror('Error: ','Failed to generated caption')
def query_image_caption(filename):
    try:
        output = query(filename)
        return output[0]['generated_text']
    except Exception as e:
        print("Error ",e)
        return None
root =tk.Tk()
root.title("Image captioning")
browse_button=tk.Button(root,text="Browse Image",command=browse_file)
browse_button.pack(pady=10)
image_label=tk.Label(root)
image_label.pack(pady=10)
result_label=tk.Label(root,text="Caption will appear here",wraplength=400,justify="left")
result_label.pack(pady=10)
root.mainloop()

