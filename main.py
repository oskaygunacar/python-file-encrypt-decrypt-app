import tkinter as tk
from tkinter import messagebox
import base64


# functions
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt_notes(): # save & Encrypt Button function
    title = title_entry.get()
    message = secret_text_panel.get("1.0", tk.END)
    master_key = master_key_entry.get()

    if len(title) == 0 or len(message) == 0 or len(master_key) == 0:
        tk.messagebox.showinfo('Error', 'Please enter all info')
    else:
        encrypted_message = encode(master_key, message)
        try:
            with open('mysecret.txt', 'a') as data_file:
                data_file.write(f'\n{title}\n{encrypted_message}')
        except:
            with open('mysecret.txt', 'w') as data_file:
                data_file.write(f'\n{title}\n{encrypted_message}')

        finally:
            title_entry.delete(0, tk.END)
            secret_text_panel.delete("1.0", tk.END)
            master_key_entry.delete(0,tk.END)

def decode_note(): # decrypt buton function
    enc_message = secret_text_panel.get("1.0", tk.END)
    master_key = master_key_entry.get()
    if len(enc_message) == 0 or len(master_key) == 0:
        tk.messagebox.showwarning('Error', 'Please fulfill all necessary information')
    else:
        try:
            decoded_message = decode(master_key, enc_message)
            secret_text_panel.delete("1.0", tk.END) # secret text alanını temizliyoruz
            master_key_entry.delete(0,tk.END) # master key alanını temizliyoruz
            secret_text_panel.insert("1.0", decoded_message)
        except:
            tk.messagebox.showwarning(title='Error', message='Please enter encrypted message!')

### Program - UI #####

window = tk.Tk()
window.title('Secret Notes')
window.minsize(width=600, height=450)
window.config(background='azure3', padx=50, pady=50)

# Image
photo_image = tk.PhotoImage(file='github-logo.png')
photo_button = tk.Button(image=photo_image,state='disabled')
photo_button.pack()

"""
Image alternative -> canvas kullanılarakda resim eklenebiliyor.
canvas = Canvas(height=200 width=200)
canvas.create_image(100,100,image=photo)
canvas.pack()
"""

# title label
title_label = tk.Label(text='Enter your title', background='azure3', highlightbackground='azure3', fg='black')
title_label.pack()

# title entry
title_entry = tk.Entry(highlightbackground='azure3', background='white', width=25, fg='black')
title_entry.pack()

#secret text label
secret_text_label = tk.Label(text='Enter your secret',background='azure3', highlightbackground='azure3', fg='black')
secret_text_label.pack()

# secret text panel
secret_text_panel = tk.Text(background='white', highlightbackground='white', width=50, fg='black')
secret_text_panel.pack()

# master key label
master_key_label = tk.Label(text='Enter master key',background='azure3', highlightbackground='azure3', fg='black')
master_key_label.pack()

# master key entry
master_key_entry = tk.Entry(highlightbackground='azure3', background='white', fg='black', width=20)
master_key_entry.pack()


# save & encrypt button
save_encrpyt_button = tk.Button(text='Save & Encrypt', highlightbackground='azure3', bg='white', command=save_and_encrypt_notes)
save_encrpyt_button.pack()

# decrypt button
decrypyt_button = tk.Button(text='Decrypt', highlightbackground='azure3', bg='white', command=decode_note)
decrypyt_button.pack()

window.mainloop()