import matplotlib.pyplot as plt
import numpy as np
import genetic_algoritm as ga
import xlwt
import datetime
import input_window  # Interface
from PyQt5 import QtWidgets
import sys

cur_dataset_count = 1
dc_min = 1
dc_max = 3

dataset = list()


class App(QtWidgets.QMainWindow, input_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.init_alg)

    def init_alg(self):
        var_count = self.vars_spin.value()
        calc_count = self.calc_spin.value()
        runs_count = self.runs_spin.value()
        script_go(var_count, calc_count, runs_count)


def goNext():
    global cur_dataset_count, dc_max
    if cur_dataset_count < dc_max:
        cur_dataset_count += 1
    return cur_dataset_count


def butNext():
    goNext()
    show_plot()


def goPrev():
    global cur_dataset_count, dc_min
    if cur_dataset_count > dc_min:
        cur_dataset_count -= 1
    return cur_dataset_count


def butPrev():
    goPrev()
    show_plot()


def butBest():
    plt.close()
    fig, axes = plt.subplots()
    axes = scatterplot(axes, True)
    plt.show()


def show_plot():
    plt.close()
    fig, axes = plt.subplots()
    axes = scatterplot(axes)
    plt.show()


def scatterplot(ax, isBest=False):  # unused
    # Create the plot object
    # figures, axes = plt.subplots()
    x_label = "X"
    y_label = "Y"
    title = "Bests"
    color = "r"
    x_data = None
    y_data = None
    if isBest:
        sh = pop.cache_max

        x_data = np.zeros(shape=(sh))
        y_data = np.zeros(shape=(sh))
        for x in range(sh):
            x_data[x] = pop.cache_list[x].variables[0]
            y_data[x] = pop.cache_list[x].variables[1]
    else:
        global cur_dataset_count, dataset
        sh = dataset[cur_dataset_count].__len__()
        x_data = np.zeros(shape=(sh))
        y_data = np.zeros(shape=(sh))
        for x in range(sh):
            x_data[x] = dataset[cur_dataset_count][x][0]
            y_data[x] = dataset[cur_dataset_count][x][1]
            pass
        title = "Generation " + cur_dataset_count.__str__()

    ax.scatter(x_data, y_data, s=10, color=color, alpha=0.75)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return ax


def start_window():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


def script_go(var_count=2, calc_count=10000, run_count=30):
    # vars
    init_count = 30
    max_count = 30
    # var_count = 2
    bord = [-5.12, 5.12]
    bord_all = np.zeros(shape=(var_count, 2))
    for x in range(var_count):
        bord_all[x, :] = bord
    # calc_count = 100000
    # run_count = 30

    # output
    # Initialize a workbook
    book = xlwt.Workbook(encoding="utf-8")
    # Add a sheet to the workbook
    sheet = book.add_sheet("Values")

    pop = None
    for x in range(run_count):
        pop = ga.Population(init_count, max_count, var_count, bord_all, calc_count)
        best = pop.cache_list[0]
        print("Gen " + x.__str__() + ":")
        print(best)
        sheet.write(x, 0, best.value.__str__())
    # info
    now = datetime.datetime.now()
    ns = now.strftime("%Y-%m-%d %H:%M:%S")
    s_info = book.add_sheet("Info")
    s_info.write(0, 0, "Date-time")
    s_info.write(0, 1, ns)

    s_info.write(1, 0, "Function")
    s_info.write(1, 1, "Rastrigin")

    s_info.write(2, 0, "Var count")
    s_info.write(2, 1, var_count.__str__())

    s_info.write(3, 0, "Calculation count")
    s_info.write(3, 1, calc_count.__str__())

    alg_inf = "Original Shard Algorithm, version 1, developed by Vasiliev Dmitriy, September 2019"
    s_info.write(0, 3, alg_inf)

    book.save("results_u-test.xls")

    # show
    dc_min = 0
    cur_dataset_count = 0
    dc_max = pop.gen_history.__len__() - 1
    global dataset
    dataset = list()
    for x in pop.gen_history:
        inds_vars = list()
        for i in x:
            inds_vars.append(i.variables)
        dataset.append(inds_vars)

    # Window, used to single run
    '''
    win = tkinter.Tk()
    win.title(u"Genetic Algorithm")
    win.resizable(False, False)
    win.geometry('200x250')
    but_next = tkinter.Button(win, text='Next', width=7, height=5, command=butNext)
    but_prev = tkinter.Button(win, text='Prev', width=7, height=5, command=butPrev)
    but_bests = tkinter.Button(win, text='Bests', width=14, height=3, command=butBest)
    but_next.place(x=100, y=10)
    but_prev.place(x=20, y=10)
    but_bests.place(x=40, y=100)
    show_plot()
    win.mainloop()
    '''


start_window()
