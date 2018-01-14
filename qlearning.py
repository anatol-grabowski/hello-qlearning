import pyqtgraph as pg
import numpy as np
import time

win = pg.GraphicsWindow()
vb = win.addViewBox(col=0, row=0)

def draw_board():
    vb.clear()
    for j, row in enumerate(board):
        for i, cell in enumerate(row):
            r = pg.QtGui.QGraphicsRectItem(i, -j, 0.9, 0.9)
            r.setPen(pg.mkPen((0, 0, 0, 100)))
            if cell == 'o':
                r.setBrush(pg.mkBrush((50, 50, 200)))
            elif cell == '+':
                r.setBrush(pg.mkBrush((50, 255, 50)))
            elif cell == '-':
                r.setBrush(pg.mkBrush((255, 50 , 50)))
            else:
                r.setBrush(pg.mkBrush((50, 50, 50)))
            vb.addItem(r)

            if cell == ' ': continue
            color = (255, 255, 255)
            t_up = pg.TextItem(str(q_matrix[i, j, 0]), color)
            t_up.setPos(i + 0.3, -j + 0.2)
            vb.addItem(t_up)
            t_dn = pg.TextItem(str(q_matrix[i, j, 1]), color)
            t_dn.setPos(i + 0.3, -j + 0.9)
            vb.addItem(t_dn)
            t_lt = pg.TextItem(str(q_matrix[i, j, 2]), color)
            t_lt.setPos(i + 0.6, -j + 0.6)
            vb.addItem(t_lt)
            t_rt = pg.TextItem(str(q_matrix[i, j, 3]), color)
            t_rt.setPos(i + 0.0, -j + 0.6)
            vb.addItem(t_rt)
    
    r = pg.QtGui.QGraphicsRectItem(actor_pos[0] + 0.1, -actor_pos[1] + 0.1, 0.7, 0.7)
    r.setPen(pg.mkPen((0, 0, 0, 100)))
    r.setBrush(pg.mkBrush((255, 255, 0, 100)))
    vb.addItem(r)


def make_action(act):
    x, y = actor_pos
    new_x, new_y = actor_pos.copy()
    if act == 0: new_y += 1
    if act == 1: new_y -= 1
    if act == 2: new_x += 1
    if act == 3: new_x -= 1
    if (new_x >= 0 and new_x < len(board[0]) and
        new_y >= 0 and new_y < len(board) and
        board[new_y][new_x] != ' '):
        actor_pos[0] = new_x
        actor_pos[1] = new_y

    cell = board[actor_pos[1]][actor_pos[0]]

    # Q[s] = Q[s] + learning_rate * (reward[s->s+1] + shortterm_preference * max(Q[s+1]) - Q[s])
    alpha = 0.5
    lambd = 0.5
    reward = -0.04
    if cell == '+': reward = 1
    if cell == '-': reward = -1
    max_new_q = q_matrix[actor_pos[0], actor_pos[1]].max()
    q = q_matrix[x, y, act]
    q_matrix[x, y, act] += alpha * (reward + lambd * max_new_q - q)
    if cell in '+-': actor_pos[:] = default_pos


def pick_best_action():
    best_action = q_matrix[actor_pos[0], actor_pos[1]].argmax()
    return best_action


def handle_kb(evt):
    if evt.key() == pg.QtCore.Qt.Key_J: act = 0
    if evt.key() == pg.QtCore.Qt.Key_K: act = 1
    if evt.key() == pg.QtCore.Qt.Key_L: act = 2
    if evt.key() == pg.QtCore.Qt.Key_H: act = 3
    if evt.key() == pg.QtCore.Qt.Key_A: act = pick_best_action()
    make_action(act)
    draw_board()

board = ['ooo+',
         'o o-',
         'oooo']
default_pos = [0, 2]
actor_pos = default_pos.copy()
q_matrix = np.zeros((len(board[0]), len(board), 4))

draw_board()
win.keyPressEvent = handle_kb
pg.QtGui.QApplication.exec_()

