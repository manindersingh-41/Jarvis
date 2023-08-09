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

    def weather():
        global temp
        global humidity
        global wind_speed
        res = requests.get('https://ipinfo.io/')
        data = res.json()

        location = data['loc'].split(',')
        latitude = location[0]
        longitude = location[1]
        

        print('weather')

        url = "http://api.openweathermap.org/data/2.5/weather?lat=29.503938&lon=76.868997&appid=0c42f7f6b53b244c78a418f4f181282a&units=metric".format(latitude, longitude)

        res = requests.get(url)


        data = res.json()


        temp = data['main']['temp']
        humidity=data['main']['humidity']
        wind_speed = data['wind']['speed']
        ''' Weather end   Weather end   Weather end    Weather end    Weather end      Weather end   Weather end'''

  
    def youtube(command):
        if 'play' in command:
            command=command.replace("play","")
        if 'song' in command:
            command=command.replace("song","")
        while 'open youtube' in command:
            speak("opening youtube")
            webbrowser.open("https://www.youtube.com/")
            current_window=GetWindowText(GetForegroundWindow()).lower()
            break
        else:
            command=command.replace("on youtube","")
            kit.playonyt(command)


    def how_to(command):
        max_results = 1
        result=search_wikihow(command, max_results)
        assert len(result) == 1
        result[0].print()
            

        speak(result[0].summary)


    def switch_window( command):
        found=0
        '''to get name from user correctly'''
        while found!=1:
            

            if 'switch' in command:
                command=command.replace("switch","")
            if 'to' in command:
                command=command.replace("to","")
            if 'change' in command:
                command=command.replace('change',"")
            if " " in command:
                command=command.replace(" ","")
            if 'bray' in command or 'bravebrowser' in command:
                command = 'brave'
            
            
            # all_win=pgw.getAllTitles()
            # command_command=command.split()
            # for q in command_command:
            #     for w in all_win:
            #         win=w.split()
            #         for fin in win:
            #             if q==fin.lower():
            #                 command=fin
                


            print(command)
            switcher=str(pgw.getWindowsWithTitle(command)).split('(')         # here ['[Win32Window', 'hWnd=66596), Win32Window', 'hWnd=1247060)]']
            print('here',len(switcher))
            print(type(switcher))
            print(switcher)
            print('end')
            ''' switcher = [Win32Window(hWnd=66752)] ''' #example
            
            
            if switcher=="'[]'":
                speak('speak again')

                '''pipe down msg here'''
                listen_q.put('switching')
                command = custom_comm_q.get()
                # command=take_command('listen switch')
                # command=command
                continue
            elif len(switcher)>2:
                switcher = switcher[1].split(',')
                # print('eliffff      ',switcher )
                switcher = switcher[0].replace('=','')
                hwdn_id = 'a'
                found = 1
                
            elif len(switcher) == 2:
                # print('1 index  :  ',switcher[1])
                switcher=switcher[1].replace('='," ")
                hwdn_id='a'
                found =1
                # speak("speak window name again")
                # command=take_command('listen switch').lower()
                # command=command
                # continue

            for i in switcher:
                if i.isdigit():
                    hwdn_id=hwdn_id+i
                    
            hwdn_id = hwdn_id.replace('a',"")
            hwdn_id = int(hwdn_id)
            # print("'",hwdn_id,"'")
            # print('win32gui.SetForegroundWindow(',hwdn_id,')')
            win32gui.SetForegroundWindow(hwdn_id) #66596

    def tell_time(command):
        strtime=datetime.datetime.now().strftime("%H:%M")
        print(strtime)
        speak(strtime)

    # check for command
    if (any(comm in command for comm in["what's time",'the time'])):
        tell_time(command)

    elif (any(comm in command for comm in["what is your name","what's your name"])):
        speak('my name is Jarvis.  Maninder Singh created me')
    
    elif (any(comm in command for comm in["switch to",'change to'])):
        switch_window(command) 

    elif 'play' in command and "on youtube" in command or 'play' in command and "in youtube" in command or 'open youtube' in command or 'on youtube' in command:
        youtube(command)   

    elif "how to" in command:
        how_to(command)



if __name__ == "__main__":
    listener_thread = threading.Thread(target=listener,args=('listening...',))
    listener_thread.start()
    commands_list()


