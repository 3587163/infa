# coding: utf-8
# license: GPLv3

import tkinter
import matplotlib as plt
plt.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *


perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

graph_window_flag = False
V_planet = []
L_distance = []
times = [0]
root2 = None
canvas = None
ax_1, ax_2, ax_3 = None, None, None

count = 0


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    Заполняет массивы скорости планеты, расстояния до звезды, время для построения графиков
    """
    global physical_time
    global displayed_time
    global graph_window_flag
    global V_planet, times, count
    global L_distance
    
    recalculate_space_objects_positions(space_objects, 10**(-2)*time_step.get())
    for body in space_objects:
        update_object_position(space, body)
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + "  milliseconds gone")

    if perform_execution:
        for obj in space_objects:
            r_star = [0, 0]
            r_planet = [0, 0]
            space.delete(obj.image)
            if obj.type == 'star':
                r_star = [obj.x, obj.y]
                create_star_image(space, obj)
            elif obj.type == 'planet':
                r_planet = [obj.x, obj.y]
                create_planet_image(space, obj)
                V_planet.append((obj.Vx**2+obj.Vy**2)**0.5)
                times.append(times[-1]+time_step.get())
                #print(obj.Vy)

        r = ((r_star[0] - r_planet[0])**2 + (r_star[1] - r_planet[1])**2)**0.5
        L_distance.append(r)

    if perform_execution:
        count += 1

        if (count % 50 == 0) and graph_window_flag:
            draw_graph()
        
        space.after(25 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def draw_graph():
    """Строит графики скорости планеты от времени, расстояния до звезды от времени, скорости от расстояния
    """
    global V_planet, L_distance, times
    global canvas
    global ax_1, ax_2, ax_3
    
    ax_1.clear()
    ax_1.set_xlabel('t')
    ax_1.set_ylabel("V(t)")
    ax_1.plot(times[1:], V_planet, color="blue", marker=".", linestyle="", markersize = 1)

    ax_2.clear()
    ax_2.set_xlabel('t')
    ax_2.set_ylabel("L(t)")
    ax_2.plot(times[1:], L_distance, color="blue", marker=".", linestyle="", markersize = 1)

    ax_3.clear()
    ax_3.set_xlabel('L')
    ax_3.set_ylabel("V(L)")
    ax_3.plot(L_distance, V_planet, color="blue", marker=".", linestyle="", markersize = 1)
    canvas.draw()
    
    

def create_graph_window():
    """Открывает новое окно в котором рисуются графики
    """
    global root2, canvas
    global graph_window_flag
    global ax_1, ax_2, ax_3

    root2 = tkinter.Tk()

    figure = Figure(figsize=(4, 4), dpi=100)
    
    ax_1 = figure.add_subplot(3, 1, 1)
    ax_2 = figure.add_subplot(3, 1, 2)
    ax_3 = figure.add_subplot(3, 1, 3)

    canvas = FigureCanvasTkAgg(figure, root2)
    canvas.get_tk_widget().grid(row=0, column=0)

    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6)

    plt.rcParams['font.size'] = 6

    graph_window_flag = True
    draw_graph()
    root2.mainloop()


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global graph_window_flag

    print('Modelling started!')
    physical_time = 0
    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame,from_=1, to=24, variable=time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    draw_graphics_button = tkinter.Button(frame, text="Draw graphics...", command=create_graph_window)
    draw_graphics_button.pack(side=tkinter.LEFT)
    
    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " milliseconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

                

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()
