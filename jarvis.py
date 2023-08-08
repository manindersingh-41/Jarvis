import pyttsx3
import speech_recognition as sr
import threading
import queue
import wikipedia as wpedia
import webbrowser
import datetime
import os
import pywhatkit as kit
import requests
import keyboard
import psutil
import time
import pyautogui as pg
from win32gui import GetWindowText, GetForegroundWindow
import screen_brightness_control as sbc
import pygetwindow as pgw  
import win32gui
from pywikihow import search_wikihow
import mysql.connector as sql
import pyperclip
import random
engine=pyttsx3.init()
# voices=engine.getProperty('voices')
# engine.setProperty('voice',voices[0].id)

command_list = []
stop_listener = 0
listen_q = queue.Queue(maxsize=1)
custom_comm_q = queue.Queue(maxsize=1)
copied_text = []



def speak(audio):
    if engine._inLoop:
        engine.endLoop()
    engine.say(audio)
    engine.runAndWait()
    # engine.endLoop()
    # engine = None
    # engine.starLoop(False)


def listener(any_msg):
    global spcl_msg
    success = 0
    listen = 0
    spcl_msg = None
    while success!=1 and stop_listener==0:
        # playsound('E:\\#####Python__Programs#####\\JARVIS\\listen3r.m4a')
        # mixer.music.play()
        recog=sr.Recognizer()

        with sr.Microphone() as source:
            listen +=1
            print(any_msg+str(listen))
                
            recog.pause_threshold=0.5
            recog.energy_threshold = 750
            recog.adjust_for_ambient_noise(source)
            recog.dynamic_energy_threshold = True
            audio=recog.listen(source)
        try:
            if listen_q.empty():
                pass
            else:
                spcl_msg = listen_q.get()
            global recog_thread
            recog_thread = threading.Thread(target=recogniser, args = (audio,spcl_msg,recog,listen))
            recog_thread.start()

            continue
            
        except Exception:
            print("Say that again please..")
            print('gonna restart')
            # speak('speak again')
            continue


def recogniser(audio,spcl_msg,recog,number):
    global stop_listener
    
    try:
        print("Recognizing..."+str(number))
        command=recog.recognize_google(audio, language='en-in')
    

        if spcl_msg == None:
            print("Recognized...")
            command=command.lower()
            print('>> you said : {}'.format(command))
            command_list.append(command)
        else:
            print("Recognized special..."+spcl_msg)
            custom_comm_q.put(command.lower())
            spcl_msg = None
        # print("You said: {}".format(command).lower())
        
        if 'end' in command:
            print(command_list)
            stop_listener = 1
    except Exception as e:
        print(e)
        # speak('say again unable to understand'+str(number))

def commands_list():
    print('Initialised command list ')
    speak('Initialised code')
    while True:
        if command_list== []:
            pass

        else:
            command = command_list.pop(0)
            if command == None:
                pass
            elif 'end program' in command or 'stop program' in command:
                '''end listener thread'''
                pass

            else:
                threading.Thread(target=tasks, args=(command,)).start()
    
    
def tasks(command):
    print('command : ', command)




if __name__ == "__main__":
    listener_thread = threading.Thread(target=listener,args=('listening...',))
    listener_thread.start()
    commands_list()


