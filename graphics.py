import random
import time
from tkinter import Tk, Canvas, PhotoImage


SQUARE_SIZE = 100  # num of pixels for square size
MARGIN      = 3


class Graphics:
    def __init__(self, m=3, n=0, s=""):
        self.matrix = self.init_matrix(m, n, s)
        self.tk = Tk()
        width = len(self.matrix[0])*SQUARE_SIZE + MARGIN
        height = len(self.matrix)*SQUARE_SIZE + MARGIN
        self.canvas = Canvas(width=width, height=height)
        self.init_tk()
        self.init_places()

    def init_matrix(self, m, n, s):
        if n == 0:
            n = m
        self.matrix = [[j+i*n for j in range (n)] for i in range(m)]
        if s != "":
            self.set_matrix(s)
        return self.matrix
    
    def set_matrix(self, s):
        vals = list(map(int, s.split('-')))
        rows, cols = len(self.matrix), len(self.matrix[0])
        if len(vals) != rows * cols:
            raise ValueError("Cann't set matrix({},{}) with {}".format(rows, cols, s))
        for i in range(rows):
            for j in range(cols):
                self.matrix[i][j] = vals[i*cols + j]


    def init_tk(self):
        self.tk.resizable(0, 0)
        self.tk.wm_attributes('-topmost', 1)
        self.canvas.pack()
        self.tk.update()

    def init_places(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        for i in range(rows):
            for j in range(cols):
                val = self.matrix[i][j]
                img = PhotoImage(file='imgs/{}.gif'.format(val))
                x = j * SQUARE_SIZE + MARGIN
                y = i * SQUARE_SIZE + MARGIN
                img_id = self.canvas.create_image((x,y), image=img, anchor='nw')
                self.matrix[i][j] = Square(val, img, img_id)
                if val == 0:
                    self.zpos = (i,j)
                self.tk.update()

    def move(self, v):
        if v not in self.actions:
            return
        vectors = {'up':(-1,0), 'down':(1,0), 'left':(0,-1), 'right':(0,1)}
        d = vectors[v]
        i,j = self.zpos
        i2,j2 = i+d[0],j+d[1]
        self.zpos = (i2,j2)
        # move(exchange)
        s1 = self.matrix[i][j]
        s2 = self.matrix[i2][j2]
        self.exchange(s1, s2)

    def exchange(self, s1, s2):
        self.canvas.itemconfig(s1.img_id, image=s2.img)
        self.canvas.itemconfig(s2.img_id, image=s1.img)
        s1.val, s2.val = s2.val, s1.val
        s1.img, s2.img = s2.img, s1.img
        self.tk.update_idletasks()
        self.tk.update()


    @property
    def actions(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        i,j = self.zpos
        results = []
        if i > 0: results.append('up')
        if i < rows-1: results.append('down')
        if j > 0: results.append('left')
        if j < cols-1: results.append('right')
        return results

    def shuffle(self, n=100):
        for _ in range(n):
            v = random.choice(self.actions)
            self.move(v)
            time.sleep(.1)

    def value(self):
        vals = []
        for row in self.matrix:
            for s in row:
                vals.append(str(s.val))
        return '_'.join(vals)

  
class Square:
    def __init__(self, val, img, img_id):
        self.val = val
        self.img = img
        self.img_id = img_id
