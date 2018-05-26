from parser import buildAST
from tokens import tokens
import pyautogui
from time import sleep

def get_mouse_x():
    return pyautogui.position()[0]

def get_mouse_y():
    return pyautogui.position()[1]

def set_mouse_x(x):
    pyautogui.moveTo(x, None)

def set_mouse_y(y):
    pyautogui.moveTo(None, y)

def click_mouse():
    pyautogui.click()

def type_keyboard(chars):
    pyautogui.typewrite(chars, interval=0.25)



def interpret(code):
    tokns = list(tokens(code))
    ast = buildAST(tokns)
    memory = {}
    functions = {'print': print,
                 'getX': get_mouse_x,
                 'getY': get_mouse_y,
                 'setX': set_mouse_x,
                 'setY': set_mouse_y,
                 'click': click_mouse,
                 'type': type_keyboard,
                 'delay': sleep}
    ast.eval(memory, functions)
