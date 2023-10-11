from pynput.keyboard import Controller, Key
from time import sleep

keyboard = Controller()

def click_search_name():
    keyboard.type("dm 1011275388489580595 churumelinho")
    sleep(0.5)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

sleep(5)
while True:
    click_search_name()
