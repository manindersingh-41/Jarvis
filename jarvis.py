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



    def open_apps(command):
        # app_web = {'app':['store','paint','clock'],'website':}
        apps = {('file explorer','files','explorer','my files'):'start explorer','powershell':'start powershell','cmd':'start cmd','whatsapp':'start whatsapp://','chrome':'start chrome','brave':'start brave','calculator':'start calc','camera':'start microsoft.windows.camera:','store':'start ms-windows-store','paint':'start ms-paint:','clock':'start ms-clock:'}
        
        
        for key in apps.keys():
            if type(key) == str:
                if key in command:
                    print('in else ',key)   
                    os.system(apps[key])
                    break
            else:
                for k in key:
                    if k in command:
                        print('for tuple : ',k)
                        os.system(apps[key])    # key is whole tuple whose value is what we want
                        break

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
        global paused
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
            paused = False
            play_pause_music(paused)
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
                
                continue
            elif len(switcher)>2:
                switcher = switcher[1].split(',')
                
                switcher = switcher[0].replace('=','')
                hwdn_id = 'a'
                found = 1
                
            elif len(switcher) == 2:
                # print('1 index  :  ',switcher[1])
                switcher=switcher[1].replace('='," ")
                hwdn_id='a'
                found =1
                

            for i in switcher:
                if i.isdigit():
                    hwdn_id=hwdn_id+i
                    
            hwdn_id = hwdn_id.replace('a',"")
            hwdn_id = int(hwdn_id)
            
            win32gui.SetForegroundWindow(hwdn_id) #66596


    def wikipedia( command):
        speak("Searching wikipedia")
        command=command.replace("wikipedia","")
        results = wpedia.summary(command,sentences=2)
        speak("according to wikipedia")
        print(results )
        speak(results)

    def notepad(command):
        if 'open'in command:
            speak('opening notepad')
            os.system('notepad')
        else:
            pass

    def copy_clipboard():
        pg.hotkey('ctrl','c')
        time.sleep(0.1)
        return pyperclip.paste()

    def copy_and_note(command):
        
        if (any(comm in command for comm in ['copy it','make a note of selected','copy and make note','copy this','make note of it','store this','store it','store the selected','copy the selected']) and not (any(comm in command for comm in ['give me all text copied','all text copied','make file of text copied','make file of text copy','create file of copy text']))):
            text = copy_clipboard()
            copied_text.append(text)
            speak(random.choice(['okay','done']))
        
        elif(any(comm in command for comm in ['give me copied text','make file of the copy text','give me all text copied','all text copied','make file of text copied','make file of text copy','create file of copy text','create file of copied text','Paste data in file'])):

            if copied_text == []:
                speak('nothing is copied')
            else:    
                speak('what should be name of file :')
                listen_q.put('copy text')
                command = custom_comm_q.get()
                global spcl_msg
                spcl_msg = None
                speak('creating file '+command)
                path_copied_text = 'C:\\Users\\manin\\OneDrive\\Desktop\\Jarvis\\'
                with open(path_copied_text+command+'.txt','w') as f:
                    for i in copied_text:
                        f.write(i+'\n')

                    copied_text.clear()
                    f.close()
                os.startfile(path_copied_text+command+'.txt')


    def groove( command):
        if 'open' in command:
            speak("opening")
            os.system("start mswindowsmusic:")
            current_window=GetWindowText(GetForegroundWindow()).lower()
        elif 'play music' in command or 'play songs' in command:
            speak("playing music")
            music_dir='E:\\Maninder Singh\\mere gaane'
            songs=os.listdir(music_dir)
            
            os.startfile(os.path.join(music_dir,songs[110]))


    def battery(command):
        pecentage = str(psutil.sensors_battery().percent)+" % remaining"
        speak(pecentage)
        if psutil.sensors_battery().power_plugged:
            speak("Also laptop is being charged")
        else:
            pass

    def brightness( command):
        chek_digit=[int(i) for i in command.split() if i.isdigit()]
        for i in chek_digit:
            value=i
        if chek_digit==[]:
            value=10

        caution=sbc.get_brightness()

        if 'increase' in command:
            if caution==100:
                speak("brightness is maximum")
            else:
                current_brightness=sbc.set_brightness("+"+str(value))
                speak("Brightness changed to "+str(current_brightness))
            
        elif 'decrease' in command:
            if caution==0:
                speak("brightness is already minimum")
            else:
                current_brightness=sbc.set_brightness("-"+str(value))
                speak("Brightness changed to "+str(current_brightness)) 

        elif 'set' in command or 'change' in command:
            if chek_digit==[]:
                value=50

            elif chek_digit>100:
                speak("can,t set brightness more than 100")
                speak("setting brightness to 100") 
                sbc.set_brightness("100")
            elif chek_digit<0:
                speak("can,t set brightness less than 0")
                speak("setting brightness to 0") 
                sbc.set_brightness("0")
            else:
                current_brightness=sbc.set_brightness(command)
                speak("Brightness changed to "+str(current_brightness))


    def open_websites(command):
        if '.com' in command or '.con' in command or '.in' in command or '.org' in command:
            if '.con' in command:
                command=command.replace('.con','.com')
            if 'open ' in command:
                command=command.replace('open ','')
            webbrowser.open('https://'+command)
        
    def tell_time(command):
        strtime=datetime.datetime.now().strftime("%H:%M")
        print(strtime)
        speak(strtime)
    
    def play_pause_music(command):
        global paused
        if paused == True and (any(comm in command for comm in ['resume','resume playing','unpause'])):
            paused = False
            keyboard.press_and_release('play/pause media')

        if paused == False and (any(comm in command for comm in ['pause','stop playing','stop music','stop sound','pause sound'])):
            paused = True
            keyboard.press_and_release('play/pause media')

    def volume(command):
        if mute == False and 'mute' in command:
            keyboard.press_and_release('volume mute')
            mute = True
         
        elif mute == True and 'unmute' in command:
            keyboard.press_and_release('volume mute')
            mute = False


    def system_fn( command):
        if 'shutdown' in command:
            speak("starting to shutdown in 5 seconds")
            time.sleep(5)
            os.system("shutdown /s /t 5")
        
        elif 'restart pc' in command or "restart system" in command:
            speak("restarting")
            time.sleep(2)
            os.system('shutdown /r /t 5')

        elif 'go to sleep' in command or 'sleep mode' in command:
            os.system("rund1132.exe powrprof,dll,SetSuspendState 0,1,0")

    
    def search_folder(parent,find_folder):
        found_f = False
        if len(parent) ==1:
            root_drive = parent+':\\'
            if os.path.exists(root_drive):
                parent = parent+':\\'
            else:
                print('drive doesnt exist on system')
                return None
        for root,directory,folder in os.walk(parent):
            if found_f:
                break
            
            for folders in directory:
                # print(folders)
                
                if find_folder in folders.lower():
            
                
                    folder_path = os.path.join(root,folders)
                    return folder_path
                
  
    def quit():
        global stop_listener
        global main_th
        stop_listener =1
        main_th = 1


    # while True:
    if (any(comm in command for comm in["what's time",'the time'])):
        tell_time(command)

    elif (any(comm in command for comm in['resume','unpause','pause','stop playing','resume playing','stop music','stop sound','pause sound'])):
        play_pause_music(command)

    elif (any(comm in command for comm in ['mute','unmute','increase volume','set volume','decrease volume'])):
        volume(command)

    elif (any(comm in command for comm in["search",'on google']) and not (any(comm in command for comm in['wikipedia']))):
        command = command.replace('search','')
        if ' on google' in command:
            command = command.replace(' on google','')
        speak('searching')
        kit.search(command)
        

    elif (any(comm in command for comm in ['copy it','copy the text','make a note of selected','copy and make note','copy this','make note of it','store this','store it','store the selected','copy the selected','give me all text copied','all text copied','make file of text copied','make file of text copy','create file of copy text'])):
        copy_and_note(command)

    elif (any(comm in command for comm in["what is your name","what's your name"])):
        speak('my name is Jarvis.  Maninder Singh created me')
    
    elif (any(comm in command for comm in["switch to",'change to'])):
        switch_window(command)
    
    elif 'quit' in command or 'sleep now' in command:
        speak('going to sleep mode for now')
        quit()
    
    elif (any(comm in command for comm in["how is the weather",'whats the weather','weather outside','what is weather',"how's weather",'how is weather'])):
        weather()
    
    elif 'wikipedia' in command:
        wikipedia()

    elif 'play' in command and "on youtube" in command or 'play' in command and "in youtube" in command or 'open youtube' in command or 'on youtube' in command:
        youtube(command)
    
    elif (any(comm in command for comm in["open notepad",'notepad'])):
        notepad()
    
    elif "how to" in command:
        how_to(command)

    elif (any(comm in command for comm in["shutdown",'restart pc','restart system','go to sleep'])):
        system_fn(command)

    elif (any(comm in command for comm in["open desktop",'go to desktop'])):
        keyboard.press_and_release('win+d')
    
    elif (any(comm in command for comm in["open groove",'play some music','open music player','play music','play songs'])):
        groove(command)
    
    elif (any(comm in command for comm in["next window",'switch window'])):
        keyboard.press_and_release('alt+tab')

    elif (any(comm in command for comm in["what is battery percentage",'battery percentage','tell battery percentage','tell battery level'])):
        battery(command)
    
    elif (any(comm in command for comm in["increase brightness",'decrease brightness','set brightness'])):
        brightness(command)

    elif 'open' in command :
        open_apps(command)



if __name__ == "__main__":
    listener_thread = threading.Thread(target=listener,args=('listening...',))
    listener_thread.start()
    commands_list()


