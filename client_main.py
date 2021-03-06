#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
import math
import time
import random as rnd
from tkinter.filedialog import *
import connection as con
from Mage_class import BASIC_ENERGY, BASIC_HEALTH
from PIL import Image, ImageTk
import images as img
import Spell_book as sb
from playsound import playsound
ANIM_DT = 10
DT = 50
"""тик времени"""
header_font = "Arial-16"
"""Шрифт в заголовке"""
cell_size = 34
"""Размер клетки"""
width = 15
"""ширина в клетках"""
window_width = width * cell_size
"""Ширина окна"""
height = 15
window_height = height * cell_size
"""Высота окна"""
interface_height = 100



class Object:
    """
    Класс объекта на экране
    Хранит координаты в пикселях, id объекта как объекта на сервере, id картинки, id на canvas
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.client_id = None
        self.img_id = None
        self.canvas_id = None


def pass_event(event):
    pass


def pass_event(event):
    pass


def read_message():
    """
    считывает сообщение с сервера
    """
    message = con.read_message(CONN)
    return message


def send_message(message):
    """
    отправляет данные на сервер
    """
    con.write_message_client(CONN, message)


def click_processing(event):
    """Обрабывает данные от клика. Дописывает в строку, строку добавляет в массив """
    # playsound('sounds/select.wav')
    event_x = event.x // 34
    event_y = event.y // 34
    message_to_server = 'click ' + str(event_x) + ' ' + str(event_y) + ' '
    send_message(message_to_server)


def key_processing(event):
    """Обрабатывает нажатие на клавишу"""
    key = event.char
    message_to_server = 'key ' + key
    send_message(message_to_server)


def play_sound(sound):
    playsound('sounds/' + sound + '.wav', False)

class Object:
    """
    Класс объекта на экране
    Хранит координаты в пикселях, id объекта как объекта на сервере, id картинки, id на canvas
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.client_id = None
        self.img_id = None
        self.canvas_id = None

    def set_coords(self, x, y):
        self.x = x
        self.y = y


class ClientGameApp:
    """Основной класс прлиожения"""
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Magic!")
        self.field = tkinter.Canvas(self.root, width=window_width, height=window_height, bg="black")
        self.interface = tkinter.Canvas(self.root, width=window_width, height=interface_height, bg="black")
        self.interface.pack(fill=tkinter.BOTH, expand=1, side=BOTTOM)
        self.field.pack(fill=tkinter.BOTH, expand=1)
        self.objects = {}
        self.health_bar1_id = None
        self.health_bar2_id = None
        self.energy_bar1_id = None
        self.energy_bar2_id = None
        self.player1_turn_id = None
        self.player2_turn_id = None
        self.range_circle_id = None
        self.action_ids = []
        self.action_number_ids = []
        self.action_bar_id = None
        self.action_cursor_id = None
        self.side = None

    def draw_object(self, obj, canv):
        """
        Рисует объект obj на canv
        Возвращает id на канвасе
        """
        if canv == 'field':
            canvas_id = self.field.create_image(obj.x, obj.y, anchor=NW, image=img.get_image(obj.img_id))
        elif canv == 'interface':
            canvas_id = self.interface.create_image(obj.x, obj.y, anchor=NW, image=img.get_image(obj.img_id))
        return canvas_id

    def animate_object(self, obj_id, x2, y2, animation_time):
        """
        Передвигает уже нарисованные объект
        :param obj_id: id объекта в массиве objects
        """
        self.unbind_all()
        screen_x1 = self.objects[obj_id].x
        screen_y1 = self.objects[obj_id].y
        screen_x2 = x2 * cell_size
        screen_y2 = y2 * cell_size
        self.move(obj_id, screen_x1, screen_y1, screen_x2, screen_y2, animation_time, 0)

    def delete_action_bar(self):
        for id in self.action_ids:
            self.interface.delete(id)
        for id in self.action_number_ids:
            self.interface.delete(id)
        self.interface.delete(self.action_bar_id)
        self.interface.delete(self.action_cursor_id)

    def set_side(self, side):
        if side == 'left':
            self.interface.create_rectangle(55, 55, 55 + cell_size, 55 + cell_size, outline='green')
            self.side = 'left'
        elif side == 'right':
            self.interface.create_rectangle(window_width - 55, 55, window_width - 55 - cell_size, 55 + cell_size, outline='green')
            self.side = 'right'

    def move(self, obj_id, screen_x1, screen_y1, screen_x2, screen_y2, animation_time, cr_time):
        cr_time += ANIM_DT
        x = screen_x1 + (screen_x2 - screen_x1) * cr_time / animation_time
        y = screen_y1 + (screen_y2 - screen_y1) * cr_time / animation_time
        self.objects[obj_id].set_coords(x, y)
        self.field.delete(self.objects[obj_id].canvas_id)
        self.objects[obj_id].canvas_id = self.field.create_image(self.objects[obj_id].x, self.objects[obj_id].y, anchor=
        NW, image=img.get_image(self.objects[obj_id].img_id))
        if cr_time <= animation_time:
            self.root.after(ANIM_DT, lambda: self.move(obj_id, screen_x1, screen_y1, screen_x2, screen_y2, animation_time, cr_time))
        else:
            self.bind_all()

    def draw_action_bar(self):
        x0 = window_width / 2 - len(sb.spell_book) / 2 * (32 + 8)
        self.action_bar_id = self.interface.create_rectangle(x0, 55 + 32, x0 + 2 * len(sb.spell_book) / 2 * (32 + 8), 55, outline='red')
        spell_img = Object()
        spell_img.img_id = 'walk'
        spell_img.x = x0
        spell_img.y = 55
        spell_number = Object()
        spell_number.img_id = '0'
        spell_number.x = x0 + 26
        spell_number.y = 55 + 18
        canv_id = self.draw_object(spell_img, 'interface')
        self.action_ids.append(canv_id)
        canv_id = self.draw_object(spell_number, 'interface')
        self.action_number_ids.append(canv_id)
        self.action_cursor_id = self.interface.create_image(x0, 55, anchor=NW, image=img.get_image('cursor'))
        for i in range(1, len(sb.spell_book)):
            x0 += (32 + 8)
            spell_img = Object()
            spell_img.img_id = sb.spell_book[i].menu_image_id
            spell_img.x = x0
            spell_img.y = 55
            spell_number = Object()
            spell_number.img_id = str(i)
            spell_number.x = x0 + 26
            spell_number.y = 55 + 18
            canv_id = self.draw_object(spell_img, 'interface')
            self.action_ids.append(canv_id)
            canv_id = self.draw_object(spell_number, 'interface')
            self.action_number_ids.append(canv_id)

    def set_action(self, action_number):
        x = window_width / 2 - len(sb.spell_book) / 2 * (32 + 8) + action_number * (32 + 8)
        self.interface.delete(self.action_cursor_id)
        self.action_cursor_id = self.interface.create_image(x, 55, anchor=NW, image=img.get_image('cursor'))

    def draw_range_circle(self, x, y, spell_range):
        screen_x = (x + 1) * cell_size - 17
        screen_y = (y + 1) * cell_size - 17
        screen_r = spell_range * cell_size
        self.range_circle_id = self.field.create_oval(screen_x - screen_r, screen_y - screen_r, screen_x + screen_r,
                                                      screen_y + screen_r, outline='red', width=4)

    def del_range_circle(self):
        self.field.delete(self.range_circle_id)

    def draw_bars(self):

        self.health_bar1_id = self.interface.create_line(0, 15, 200, 15, width=15, fill='red')
        self.health_bar2_id = self.interface.create_line(window_width - 200, 15, window_width, 15, width=15, fill='red')
        self.energy_bar1_id = self.interface.create_line(0, 35, 200, 35, width=15, fill='grey')
        self.energy_bar2_id = self.interface.create_line(window_width - 200, 35, window_width, 35, width=15,
                                                         fill='grey')

    def draw_turn(self):
        self.player1_turn_id = self.interface.create_rectangle(5, 55, 45, 95, fill='red')
        self.player2_turn_id = self.interface.create_rectangle(window_width - 5, 55, window_width - 45, 95, fill='red')
        mage1 = Object()
        mage1.img_id = 'mage1'
        mage1.x = 55
        mage1.y = 55
        self.draw_object(mage1, 'interface')
        mage2 = Object()
        mage2.img_id = 'mage2'
        mage2.x = window_width - 55 - 32
        mage2.y = 55
        self.draw_object(mage2, 'interface')

    def set_turn(self, player):
        if player == 'player1':
            self.interface.itemconfig(self.player1_turn_id, fill='green')
            self.interface.itemconfig(self.player2_turn_id, fill='red')
        if player == 'player2':
            self.interface.itemconfig(self.player2_turn_id, fill='green')
            self.interface.itemconfig(self.player1_turn_id, fill='red')

    def set_energy(self, player, energy):
        if player == 'player1':
            self.interface.coords(self.energy_bar1_id, 0, 35, energy / BASIC_ENERGY * 200, 35)
        elif player == 'player2':
            self.interface.coords(self.energy_bar2_id, window_width - energy / BASIC_ENERGY * 200, 35, window_width, 35)

    def set_health(self, player, health):
        if player == 'player1':
            self.interface.coords(self.health_bar1_id, 0, 15, health / BASIC_HEALTH * 200, 15)
        elif player == 'player2':
            self.interface.coords(self.health_bar2_id, window_width - health / BASIC_HEALTH * 200, 15, window_width, 15)

    def end_game(self, winner):
        self.unbind_all()
        self.delete_action_bar()
        if winner == 'player1':
            phrase = 'Player 1 won!'
            if self.side == 'left':
                play_sound('win')
            else:
                play_sound('lose')
        elif winner == 'player2':
            phrase = 'Player 2 won!'
            if self.side == 'right':
                play_sound('win')
            else:
                play_sound('lose')
        label = Label(self.root, text=phrase, fg='red', bg='black', font="Arial 20")
        label.pack()
        label_window = self.interface.create_window(window_width/2 - 70, 55, anchor=NW, window=label)
    # def del_object(self, canvas_id):
    #     self.field.delete(canvas_id)

    def process_message(self, message):
        """Строку от сервера делит на слова, созвдает объеты класса Obj, записывает признаки"""
        list_of_words = message.split()
        if list_of_words[0] == 'obj':
            a = Object()
            a.client_id = int(list_of_words[1])
            a.x = int(list_of_words[2]) * cell_size
            a.y = int(list_of_words[3]) * cell_size
            a.img_id = list_of_words[4]
            if self.objects.get(a.client_id) is not None:
                self.field.delete(self.objects[a.client_id].canvas_id)
            a.canvas_id = self.draw_object(a, 'field')
            self.objects[a.client_id] = a
        if list_of_words[0] == 'del':
            self.field.delete(self.objects[int(list_of_words[1])].canvas_id)
            del self.objects[int(list_of_words[1])]
        if list_of_words[0] == 'animate':
            self.animate_object(int(list_of_words[1]), int(list_of_words[2]), int(list_of_words[3]), int(list_of_words[4]))
        if list_of_words[0] == 'set_energy':
            self.set_energy(list_of_words[1], int(list_of_words[2]))
        if list_of_words[0] == 'set_health':
            self.set_health(list_of_words[1], int(list_of_words[2]))
        if list_of_words[0] == 'set_turn':
            self.set_turn(list_of_words[1])
        if list_of_words[0] == 'draw_range_circle':
            self.draw_range_circle(int(list_of_words[1]), int(list_of_words[2]), int(list_of_words[3]))
        if list_of_words[0] == 'del_range_circle':
            self.del_range_circle()
        if list_of_words[0] == 'end_game':
            self.end_game(list_of_words[1])
        if list_of_words[0] == 'set_action':
            self.set_action(int(list_of_words[1]))
        if list_of_words[0] == 'play_sound':
            play_sound(list_of_words[1])
        if list_of_words[0] == 'side':
            self.set_side(list_of_words[1])

            
    def draw_grid(self):
        """Рисует сетку и камушки"""
        for i in range(0, window_width // cell_size + 1, 1):
            self.field.create_line(0, cell_size * i, window_height, cell_size * i, fill='grey')
            for j in range(0, window_height // cell_size + 1, 1):
                self.field.create_line(cell_size * j, 0, cell_size * j, window_width, fill='grey')

    def bind_all(self):
        self.field.bind('<Button-1>', click_processing)
        self.root.bind('<Key>', key_processing)

    def unbind_all(self):
        self.field.bind('<Button-1>', pass_event)
        self.root.bind('<Key>', pass_event)

    def update(self):
        message = read_message()
        if len(message) > 0:
            if message == '':
                pass
            else:
                self.process_message(message)
        self.root.after(DT, self.update)


def main():
    app = ClientGameApp()
    img.load_all_images(app)

    app.bind_all()
    app.draw_grid()
    app.draw_bars()
    app.draw_turn()
    app.draw_action_bar()
    app.update()
    app.root.mainloop()

"""константа связи, работает во всех случаях передачи и чтения сообщений"""
CONN = con.start_connection_client()
main()
