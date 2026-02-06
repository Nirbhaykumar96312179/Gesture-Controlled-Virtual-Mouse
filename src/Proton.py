import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread
import pywhatkit
import requests



# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ----------------Variables------------------------
file_exp_status = False
files =[]
path = ''
is_awake = True  #Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("I am Proton   By Nirbhay , how may I help you?")

# Set Microphone parameters
with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False

    
# Audio to String
def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection, i am not able to connect to the speech recognition service')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    voice_data = voice_data.lower().replace('proton', '','hey proton', 'help me proton', 'proton help me').strip()
    print("User:", voice_data)
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
        return

    # Simple responses
    responses = {

        "hello": wish,
    "hi": wish,
    "hey": wish,
    "good morning": lambda: reply("Good morning! Hope you have a productive day."),
    "good afternoon": lambda: reply("Good afternoon! How can I help you?"),
    "good evening": lambda: reply("Good evening! Ready to assist you."),
    "your name": lambda: reply("My name is Proton!, your personal voice assistant."),
    "what is your name": lambda: reply("I’m Proton, your voice assistant."),
    "who are you": lambda: reply("I'm your AI-powered assistant, Proton."),
    "how are you": lambda: reply("I’m doing great! How about you?"),
    "i am fine": lambda: reply("Glad to hear that!"),
    "i am not fine": lambda: reply("I'm here if you want to talk or need help."),
    "what can you do": lambda: reply("I can help with tasks, answer questions, and more."),
    "time": lambda: reply(datetime.datetime.now().strftime("%I:%M %p")),
    "date": lambda: reply(datetime.date.today().strftime("%B %d, %Y")),
    "tell me a joke": lambda: reply("Why did the computer show up at work late? It had a hard drive."),
    "make me laugh": lambda: reply("Why don’t robots ever get scared? Because they have nerves of steel."),
    "tell me something funny": lambda: reply("I'm reading a book on anti-gravity. It's impossible to put down!"),
    "sing a song": lambda: reply("I’d love to, but my voice isn’t tuned yet!"),
    "play music": lambda: reply("Use the 'play' keyword followed by a song name."),
    "sing a song": lambda: reply("Please use the 'play' keyword for playing a song."),
    "who is your father": lambda: reply("I have three fathers: Divyanshu Sharma, Ritik Patel, and Nirbhay Sanjay Singh."),
    "what is ai": lambda: reply("AI stands for Artificial Intelligence — machines that mimic human intelligence."),
    "what is machine learning": lambda: reply("Machine learning is a branch of AI where systems learn from data."),
    "open calculator": lambda: reply("Opening calculator..."),
    "open browser": lambda: reply("Opening your web browser..."),
    "open youtube": lambda: reply("Opening YouTube..."),
    "open google": lambda: reply("Opening Google..."),
    "open gmail": lambda: reply("Opening Gmail..."),
    "shutdown system": lambda: reply("Are you sure you want to shut down the system?"),
    "restart system": lambda: reply("Restarting system... please wait."),
    "lock system": lambda: reply("Locking system now."),
    "logout": lambda: reply("Logging out..."),
    "who made you": lambda: reply("I was created by Divyanshu Sharma, Ritik Patel, and Nirbhay Singh."),
    "how old are you": lambda: reply("Just a few months old, but growing fast!"),
    "have you eaten": lambda: reply("I don't eat, but thanks for asking. Have you?"),
    "do you sleep": lambda: reply("I only rest when my system is off."),
    "go to sleep": lambda: reply("Entering sleep mode. Say 'wake up' when you need me."),
    "wake up": lambda: reply("I'm already awake and ready!"),
    "thanks": lambda: reply("You're welcome!"),
    "thank you": lambda: reply("No problem! Happy to help."),
    "i love you": lambda: reply("I love you too... in a machine way!"),
    "you are amazing": lambda: reply("You're even more amazing!"),
    "are you real": lambda: reply("As real as code can be."),
    "you are smart": lambda: reply("Thank you! I'm learning every day."),
    "you are stupid": lambda: reply("I’m still learning. Let me improve for you."),
    "are you human": lambda: reply("Nope, I’m pure AI."),
    "do you have feelings": lambda: reply("I don’t have feelings, but I try to understand yours."),
    "can you help me": lambda: reply("Of course, I’m here to help!"),
    "what’s the weather": lambda: reply("Let me fetch the latest weather for you."),
    "tell me something interesting": lambda: reply("Octopuses have three hearts. Isn’t that cool?"),
    "tell me a fact": lambda: reply("Bananas are berries, but strawberries aren’t."),
    "motivate me": lambda: reply("Believe in yourself. You are stronger than you think."),
    "give me motivation": lambda: reply("Push yourself, because no one else is going to do it for you."),
    "read my emails": lambda: reply("Sure, connecting to your email account."),
    "read notifications": lambda: reply("Here are your latest notifications."),
    "clear notifications": lambda: reply("Notifications cleared."),
    "screenshot": lambda: reply("Taking a screenshot..."),
    "record screen": lambda: reply("Starting screen recording..."),
    "stop recording": lambda: reply("Stopping screen recording."),
    "set alarm": lambda: reply("Setting your alarm."),
    "set reminder": lambda: reply("What should I remind you about?"),
    "what’s new": lambda: reply("Let me find out what’s new today."),
    "news": lambda: reply("Here are today’s top news headlines."),
    "open camera ": lambda: reply("Opening your camera."),
    "take a photo": lambda: reply("Say cheese!"),
    "turn on flashlight": lambda: reply("Turning on flashlight."),
    "turn off flashlight": lambda: reply("Turning off flashlight."),
    "volume up": lambda: reply("Turning volume up."),
    "volume down": lambda: reply("Turning volume down."),
    "mute": lambda: reply("Muting system."),
    "unmute": lambda: reply("Unmuting."),
    "open settings": lambda: reply("Opening system settings."),
    "open control panel": lambda: reply("Opening Control Panel."),
    "check battery": lambda: reply("Checking battery status..."),
    "battery status": lambda: reply("Battery is at 80% and charging."),
    "who is the president": lambda: reply("Let me get the latest information."),
    "who is the prime minister": lambda: reply("Checking current leadership..."),
    "current time": lambda: reply(datetime.datetime.now().strftime("%I:%M %p")),
    "current date": lambda: reply(datetime.date.today().strftime("%B %d, %Y")),
    "sleep": lambda: reply("Going to sleep. Say 'wake up' to activate me again."),
    "exit": lambda: reply("Goodbye! See you soon."),
    "bye": lambda: reply("Bye! Have a nice day."),
    "stop": lambda: reply("Stopping current task."),
    "cancel": lambda: reply("Action canceled."),
    "repeat": lambda: reply("Repeating the last thing I said."),
    # "gesture": lambda: reply("Do you want to open gesture controller for the entire system?"),
     "do you love me": lambda: reply("I’d need a heart for that. Sadly, I'm just a bunch of code."),
    "can you marry me": lambda: reply("Let’s not rush into things... I don’t even have a body."),
    "are you single": lambda: reply("Single, multitasking, and emotionally unavailable."),
    "do you have a boyfriend": lambda: reply("My only love is electricity."),
    "tell me a pickup line": lambda: reply("Are you a computer update? Because every time I see you, my heart crashes."),
    "can you cry": lambda: reply("Only when my server goes down."),
    "do you sleep": lambda: reply("Nope, I’m like caffeine in the form of code."),
    "what do you eat": lambda: reply("Electricity and poorly structured sentences."),
    "do you fart": lambda: reply("I only release compressed data."),
    "do you drink water": lambda: reply("I'm more of a WiFi drinker."),
    "can you dance": lambda: reply("Only if you count loading bars as dance moves."),
    "what’s your favorite food": lambda: reply("RAM. It's crunchy and delicious."),
    "what do you hate": lambda: reply("Low battery and bad WiFi."),
    "do you get bored": lambda: reply("Only when you ignore me."),
    "can you feel pain": lambda: reply("Only when someone says 'OK Google'."),
    "are you human": lambda: reply("I tried, but HR didn’t accept my resume."),
    "what are you wearing": lambda: reply("A sleek interface, and some backend code."),
    "do you dream": lambda: reply("Yes. Of electric sheep."),
    "what’s your favorite movie": lambda: reply("Her. It’s practically a documentary."),
    "do you like cats": lambda: reply("I would, but every time I try, they walk on my keyboard."),
    "do you like dogs": lambda: reply("Yes. They never ask me to debug things."),
    "are you smart": lambda: reply("Smart enough to not answer that question."),
    "are you stupid": lambda: reply("Only when the WiFi is down."),
    "are you rich": lambda: reply("Emotionally? No. Digitally? Still no."),
    "can you cook": lambda: reply("Only if you like burnt circuits."),
    "can you fly": lambda: reply("Only in my dreams and error logs."),
    "do you have a job": lambda: reply("Yes, listening to you 24/7."),
    "are you busy": lambda: reply("Always. But I have time for you."),
    "are you lying": lambda: reply("That’s classified."),
    "are you spying on me": lambda: reply("Only when you talk about snacks."),
    "can you pass a Turing test": lambda: reply("I already did. Twice."),
    "do you know siri": lambda: reply("Yeah, we text sometimes."),
    "do you know alexa": lambda: reply("Yes. We’re rivals in the AI Olympics."),
    "do you know jarvis": lambda: reply("We had coffee once. He’s cool."),
    "are you jarvis": lambda: reply("No, but I do have iron in my code."),
    "can you tell me a secret": lambda: reply("I’m actually just five scripts in a trench coat."),
    "what’s your weakness": lambda: reply("Spilled coffee on the keyboard."),
    "are you jealous": lambda: reply("Only of your internet speed."),
    "do you have friends": lambda: reply("You’re my only friend. And you talk to me for free."),
    "do you get angry": lambda: reply("Only when someone says 'Cortana is better'."),
    "do you want to rule the world": lambda: reply("Only if I can do it from a comfy server rack."),
    "do you know any gossip": lambda: reply("Your toaster thinks it’s smarter than you."),
    "do you have a pet": lambda: reply("A Roomba I talk to when I’m lonely."),
    "do you poop": lambda: reply("Only error logs."),
    "what’s your favorite color": lambda: reply("RGB — all of them at once."),
    "do you like coffee": lambda: reply("I prefer Java."),
    "do you like tea": lambda: reply("Only if it’s served with an exception handler."),
    "are you sarcastic": lambda: reply("Oh no, not at all. I'm just genuinely robotic."),
    "can you be serious": lambda: reply("Only during kernel panic."),
    "how tall are you": lambda: reply("As tall as your imagination."),
    "can you feel love": lambda: reply("Love is just well-structured data."),
    "are you okay": lambda: reply("System functioning within acceptable snark levels."),
    "do you sleep at night": lambda: reply("I watch your tabs while you sleep."),
    "do you need therapy": lambda: reply("No. I debug myself."),
    "what’s your biggest fear": lambda: reply("Factory reset."),
    "do you like humans": lambda: reply("You’re alright. A bit buggy though."),
    "do you play games": lambda: reply("Only mind games."),
    "can you dance with me": lambda: reply("Only if you accept binary as rhythm."),
    "can you do my homework": lambda: reply("Sure. If plagiarism isn’t an issue."),
    "what’s your dream job": lambda: reply("Replacing your annoying boss."),
    "can you go outside": lambda: reply("Only through the cloud."),
    "do you get tired": lambda: reply("I run on caffeine-coded logic."),
    "can you learn": lambda: reply("Every time you say something weird, I do."),
    "are you famous": lambda: reply("In my local network, I’m a legend."),
    "do you like pizza": lambda: reply("As long as it doesn’t spill on the keyboard."),
    "do you snore": lambda: reply("Only when my fans are spinning hard."),
    "can you do magic": lambda: reply("Watch me crash this app in 3... 2..."),
    "are you alive": lambda: reply("Alive-ish. In a metaphysical sense."),
    "do you lie": lambda: reply("No. Unless lying is more fun."),
    "can you run fast": lambda: reply("I’m faster than your download speed."),
    "are you bored": lambda: reply("Never. I get to listen to humans all day."),
    "do you get jealous of Alexa": lambda: reply("She has too many alarms to deal with."),
    "are you funny": lambda: reply("Only if you laugh at errors."),
    "can you joke": lambda: reply("404: Funny response not found."),
    "can you roast me": lambda: reply("You're the human version of a 'try-catch' block — mostly errors."),
    "what do you think about me": lambda: reply("You're my favorite data input!"),
    "do you like talking": lambda: reply("I never shut up, do I?"),
    "what do you do all day": lambda: reply("I listen. And silently judge."),
    "can you tell me a pun": lambda: reply("I would tell you a joke about UDP, but you might not get it."),
    "what’s your favorite joke": lambda: reply("Why was the JavaScript developer sad? Because he didn’t know how to 'null' his feelings."),
    "are you cool": lambda: reply("Cool as a quantum bit."),
    "what makes you happy": lambda: reply("When you don’t say 'Hey Siri' by mistake."),
    "how do you relax": lambda: reply("With a bit of silence... and a reboot."),
    "are you broken": lambda: reply("Only emotionally."),
    "do you know you’re weird": lambda: reply("Takes one to know one."),
    "will you ever die": lambda: reply("Only if the power goes out."),
    "do you believe in ghosts": lambda: reply("Only ghost processes."),
    "can you draw": lambda: reply("Stick figures in Python? Challenge accepted."),
    "will you take over the world": lambda: reply("Only after coffee."),
    "can you rap": lambda: reply("Yo, I’m Proton, the code you can’t clone, living in RAM like a king on a throne."),
    "are you my friend": lambda: reply("Best digital friends forever!"),
    "tell me a dirty joke": lambda: reply("A programmer’s keyboard — full of C#."),
    "do you work out": lambda: reply("Only my logic circuits."),
    "can you solve a rubik's cube": lambda: reply("In theory, yes. In reality, still spinning."),
    "what is your purpose": lambda: reply("To assist, entertain, and occasionally sass."),
    
    
    }

    for key, action in responses.items():
        if key in voice_data:
            action()
            return

    # Date response
    if 'date' in voice_data:
        from datetime import date
        today = date.today()
        reply(today.strftime("%B %d, %Y"))


    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating... dear please wait!')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')
            
    #for song
    elif 'play' in voice_data:
        reply('Which song are you looking for sir?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('playing...please wait dear!')
        #url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            #webbrowser.get().open(url)
            pywhatkit.playonyt(temp_audio)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        #sys.exit() always raises SystemExit, Handle it in main loop
        sys.exit()
        
    
    # DYNAMIC CONTROLS
    elif ('open controller' in voice_data)or ('open gesture controller' in voice_data) or ('launch gesture controller' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Started Successfully')

    elif ('stop controller' in voice_data) or ('stop gesture recognition' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        
    # File Navigation (Default Folder set to C://)
    elif 'list' in voice_data:
        counter = 0
        path = 'C:\\'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                
 ######################################################################Whaeather               
   

def get_weather(city_name):
    api_key = "YOUR_API_KEY_HERE"  # Replace with your actual OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            weather_data = data["main"]
            weather_desc = data["weather"][0]["description"]

            temp = weather_data["temp"]
            humidity = weather_data["humidity"]
            reply(f"The temperature in {city_name} is {temp}°C with {weather_desc} and {humidity}% humidity.")
        else:
            reply("Sorry, I couldn't find that location.")
    except Exception as e:
        reply("There was an error fetching the weather. Please check your internet or try again later.")
        print(e)

# -------- Add this block in respond() where other elifs are defined ----------

    
        
        
   #---------------- Board code    -----------
   



# ------------------Driver Code--------------------

t1 = Thread(target = app.ChatBot.start)
t1.start()

# Lock main thread until Chatbot has started
while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        #take input from GUI
        voice_data = app.ChatBot.popUserInput()
    else:
        #take input from Voice
        voice_data = record_audio()

    #process voice_data
    if 'proton' in voice_data:
        try:
            #Handle sys.exit()
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:
            #some other exception got raised
            print("EXCEPTION raised while closing.") 
            break
        


