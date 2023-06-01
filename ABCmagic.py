import time

import customtkinter as ctk
from tkinter import *
from PIL import Image
import screen_info
import pygame
import os
import random
import sys

sc_ancho, sc_alto = screen_info.get_info()
ctk.set_default_color_theme("dark-blue")
pos_x = int(sc_ancho / 2)
pos_y = int(sc_alto / 2)
pygame.mixer.init()


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GameWindow(ctk.CTkToplevel):
    letras_option = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S",
                     "T", "U", "V", "W", "X", "Y", "Z"]
    music_option = [0.0, 222, 467, 706, 1000, 1246, 1577, 1732, 2043]
    current_letter = random.choice(letras_option)
    current_direction = random.choice(["r", "l", "b"])
    left: ctk.CTkFrame
    center: ctk.CTkFrame
    right: ctk.CTkFrame
    msg: ctk.CTkFrame
    flecha_left: ctk.CTkFrame
    flecha_right: ctk.CTkFrame
    frame_letra: ctk.CTkFrame
    label_letra: ctk.CTkLabel
    label_derecha: ctk.CTkLabel
    label_izquierda: ctk.CTkLabel
    label_msg: ctk.CTkLabel
    exit_button: ctk.CTkButton
    height_top = int(sc_alto * (2 / 3))
    height_bottom = int(sc_alto * (1 / 3))
    size_letra = int(sc_ancho * (1 / 3))
    size_flechas = (int(sc_ancho * (1 / 5)), int(sc_alto * (1 / 5)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="#E6E6E6")
        self.title("Game")
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", self.end_game)
        # self.geometry(f'{sc_ancho}x{sc_alto - 300}+{pos_x- 450}+{pos_y - 300}"')
        self.wm_frames()
        self.widgets()

    def wm_frames(self):

        self.center = ctk.CTkFrame(self, fg_color='transparent', height=self.height_top)
        self.center.pack(fill='x', anchor='center', side='top')

        separador = ctk.CTkFrame(self.center, fg_color='transparent', width=int(sc_ancho/32))
        separador.grid(row=0, column=0)

        self.flecha_left = ctk.CTkFrame(self.center, fg_color='transparent', width=self.size_flechas[0], height=self.size_flechas[1])
        self.flecha_left.grid(row=0, column=1)
        self.frame_letra = ctk.CTkFrame(self.center, fg_color='transparent', width=self.size_letra, height=self.size_letra)
        self.frame_letra.grid(row=0, column=2, columnspan=2, sticky='nsew')
        self.flecha_right = ctk.CTkFrame(self.center, fg_color='transparent', width=self.size_flechas[0], height=self.size_flechas[1])
        self.flecha_right.grid(row=0, column=4, sticky='e')

        self.left = ctk.CTkFrame(self, fg_color='transparent', width=int(sc_ancho / 6) - 100)
        self.left.pack(fill='y', side='left', anchor='w')
        self.right = ctk.CTkFrame(self, fg_color='transparent', width=int(sc_ancho / 6) - 100)
        self.right.pack(fill='y', side='right', anchor='e')
        self.msg = ctk.CTkFrame(self, fg_color='transparent')
        self.msg.pack(fill='both', side='top', anchor='center')

    def widgets(self):
        letra_name = 'Pictures\\' + self.current_letter + ".png"
        izqu_path = 'Pictures\\left.png'
        der_path = 'Pictures\\right.png'
        print(resource_path(letra_name))
        letra = ctk.CTkImage(light_image=Image.open(resource_path(letra_name)), dark_image=Image.open(resource_path(letra_name)), size=(self.size_letra, self.size_letra))
        derecha = ctk.CTkImage(light_image=Image.open(resource_path(der_path)), dark_image=Image.open(resource_path(der_path)), size=self.size_flechas)
        izquierda = ctk.CTkImage(light_image=Image.open(resource_path(izqu_path)), dark_image=Image.open(resource_path(izqu_path)), size=self.size_flechas)

        self.label_izquierda = ctk.CTkLabel(self.flecha_left, image=izquierda, text='')
        self.label_derecha = ctk.CTkLabel(self.flecha_right, image=derecha, text='')
        self.label_letra = ctk.CTkLabel(self.frame_letra, image=letra, fg_color='transparent', text='')
        self.label_msg = ctk.CTkLabel(self.msg, text="Aquí puede aparecer un mensaje", font=('Courier', 50), text_color='black', fg_color='transparent')
        self.label_letra.pack()
        self.change_direction()

        self.label_msg.pack(anchor='center', fill='both')

        self.exit_button = ctk.CTkButton(self.right, text="Exit", command=self.end_game)
        self.exit_button.pack(anchor='center', padx=10)

        ctk.CTkButton(self.left, text="Change", command=self.action).pack(anchor='center', padx=10)

        pass

    def change_letter(self):
        new_letter = random.choice(self.letras_option)

        while new_letter == self.current_letter:
            new_letter = random.choice(self.letras_option)

        self.current_letter = new_letter
        image_name = 'Pictures\\' + new_letter + '.png'
        nueva_imagen = ctk.CTkImage(light_image=Image.open(resource_path(image_name)), dark_image=Image.open(resource_path(image_name)), size=(self.size_letra, self.size_letra))

        # Actualizar la etiqueta con la nueva imagen
        self.label_letra.configure(image=nueva_imagen)
        self.label_letra.image = nueva_imagen  # Actualizar la referencia a la imagen

    def redefine_dir(self):
        if self.current_direction == "r":
            self.current_direction = random.choice(["l", "b"])
        elif self.current_direction == "l":
            self.current_direction = random.choice(["r", "b"])
        elif self.current_direction == "b":
            self.current_direction = random.choice(["l", "r"])

    def change_direction(self):
        if self.current_direction == "r":
            # mostrar solo imagen derecha
            self.label_derecha.pack()
            self.label_izquierda.pack_forget()
        elif self.current_direction == "l":
            # mostrar solo imagen izquierda
            self.label_izquierda.pack()
            self.label_derecha.pack_forget()
        else:
            # mostrar ambas images
            self.label_derecha.pack()
            self.label_izquierda.pack()

        self.redefine_dir()

    def action(self):
        self.change_letter()
        self.change_direction()

    def end_game(self):
        self.master.deiconify()
        self.destroy()
        pygame.mixer.music.load(resource_path('music\\funcky.mp3'))
        pygame.mixer.music.play(loops=-1, start=1.5, fade_ms=1500)


class Welcome(ctk.CTk):
    ctk.set_appearance_mode("dark")
    global pos_x, pos_y
    center: ctk.CTkFrame
    left: ctk.CTkFrame
    buttons: ctk.CTkFrame
    f_time: ctk.CTkFrame
    f_scale: ctk.CTkFrame
    f_message: ctk.CTkFrame
    w_label: ctk.CTkLabel
    button_messages: ctk.CTkButton
    button_start: ctk.CTkButton
    menubar: Menu
    messages: Menu
    music_option = [0.0, 222, 467, 706, 1000, 1246, 1577, 1732, 2043]

    def __init__(self):
        super().__init__()
        pygame.mixer.music.load(resource_path('music\\funcky.mp3'))
        pygame.mixer.music.play(loops=-1, start=1.5, fade_ms=1500)
        self.title("ABC magic")
        self.configure(fg_color='#2C3958')
        self.geometry(f"{850}x{500}+{pos_x- 450}+{pos_y - 300}")
        self.resizable(False, False)
        self.icon()
        self.frames()
        self.widgets()
        self.toplevel_window = None

    def icon(self):
        image_path = resource_path("Pictures\\icon.ico")
        self.iconbitmap(image_path)

    def frames(self):
        # frames primarios
        self.left = ctk.CTkFrame(self, fg_color="transparent", height=500, width=150)
        self.left.grid(row=0, column=1)
        self.center = ctk.CTkFrame(self, fg_color="transparent", height=500, width=500)
        self.center.grid(row=0, column=2)
        right = ctk.CTkFrame(self, fg_color="transparent", height=500, width=200)
        right.grid(row=0, column=3)

        # frames secundarios en frame center
        separador1 = ctk.CTkFrame(self.center, fg_color='transparent', width=480, height=100)
        separador1.grid(row=0, column=0)
        # etiqueta welcome .grid(row=0, column=1)
        separador2 = ctk.CTkFrame(self.center, fg_color='transparent', width=480, height=80)
        separador2.grid(row=2, column=0)
        self.buttons = ctk.CTkFrame(self.center, fg_color='transparent', width=480, height=500)
        self.buttons.grid(row=3, column=0)

        # frames secundarios en frame left
        separador3 = ctk.CTkFrame(self.left, fg_color='transparent', width=150, height=250)
        separador3.grid(row=0, column=0)
        separador4 = ctk.CTkFrame(self.buttons, fg_color='transparent', width=480, height=4)
        separador4.grid(row=1, column=0)
        separador5 = ctk.CTkFrame(self.left, fg_color='transparent', width=10, height=4)
        separador5.grid(row=2, column=0)
        separador6 = ctk.CTkFrame(self.left, fg_color='transparent', width=10, height=4)
        separador6.grid(row=4, column=0)

        # frames de configuración
        self.f_time = ctk.CTkFrame(self.left, fg_color='transparent', height=25)
        self.f_time.grid(row=1)

        self.f_scale = ctk.CTkFrame(self.left, fg_color='transparent', height=25)
        self.f_scale.grid(row=3)

        self.f_message = ctk.CTkFrame(self.left, fg_color='transparent', height=25)
        self.f_message.grid(row=5)

    def widgets(self):
        # labels
        label = ctk.CTkLabel(master=self.center, text="ABC Magic", fg_color="transparent", font=('Courier', 100), corner_radius=10, pady=20)
        label.grid(row=1, column=0)

        # buttons
        self.button_start = ctk.CTkButton(self.buttons, text="Start", border_color="black", border_width=1, command=self.start_game)
        self.button_start.grid(column=0, row=0)
        ctk.CTkButton(self.buttons, text="Exit", command=self.destroy, border_color="black", border_width=1).grid(column=0, row=2)
        self.button_messages = ctk.CTkButton(self.f_message, text="Messages", border_color="black", command=self.window_message)
        self.button_messages.pack()

        ctk.CTkLabel(self.f_time, text="Time:", fg_color='transparent', padx=7).grid(row=0, column=0)
        game_time = ctk.CTkOptionMenu(self.f_time, values=["10", "20", "30", "40"], width=50, height=20)
        game_time.grid(row=0, column=1)
        ctk.CTkLabel(self.f_time, text="minutes", fg_color='transparent', padx=7).grid(row=0, column=2)

        # scale configure
        ctk.CTkLabel(self.f_scale, text="Change:", fg_color='transparent', padx=7).grid(row=0, column=0)
        game_scale = ctk.CTkOptionMenu(self.f_scale, values=["3", "4", "5", '6'], width=50, height=20)
        game_scale.grid(row=0, column=1)
        ctk.CTkLabel(self.f_scale, text="seconds", fg_color='transparent', padx=7).grid(row=0, column=2)

    def window_message(self):
        self.button_messages.configure(state='disabled')
        self.button_start.configure(state='disabled')
        icon_path = resource_path('Pictures\\message.ico')
        w_messages = Toplevel(self)
        w_messages.iconbitmap(icon_path)
        w_messages.title('Messages Options')
        w_messages.geometry(f"300x200+{pos_x - 200}+{pos_y}")
        w_messages.transient(self)
        w_messages.focus_set()
        ctk.CTkLabel(w_messages, text="Configurar\n opciones de\n mensajes", fg_color='transparent', font=('Courier', 20), text_color='red').pack()

        def on_close():
            w_messages.destroy()
            self.button_messages.configure(state='normal')
            self.button_start.configure(state='normal')

        w_messages.protocol("WM_DELETE_WINDOW", on_close)

    def start_game(self):
        pygame.mixer.music.load(resource_path('music\\mix.mp3'))
        pygame.mixer.music.play(loops=-1, fade_ms=1000, start=random.choice(self.music_option))
        self.withdraw()
        self.toplevel_window = GameWindow(self)


def run():
    wel = Welcome()
    wel.mainloop()


if __name__ == '__main__':
    run()
