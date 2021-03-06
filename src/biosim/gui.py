__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'


from tkinter import *

class GUI:

    def __init__(self):

        root = Tk()

        label = Label(root, text='Simulation of Rossumøya')
        label.pack()
        top_frame = Frame(root)
        top_frame.pack()

        bottom_frame = Frame(root)
        bottom_frame.pack(side=BOTTOM)

        button1 = Button(top_frame, text='Start simulation', fg='red')
        button2 = Button(top_frame, text='Change parameters', fg='blue')
        button3 = Button(top_frame, text='Add population', fg='green')

        button1.pack(side=LEFT)
        button2.pack(side=LEFT)
        button3.pack(side=LEFT)

        root.mainloop()

if __name__ == '__main__':

    test = GUI()
