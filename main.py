import speech_recognition as sr
from gtts import gTTS
import playsound
import random
import os
from datetime import datetime
import webbrowser
import pyjokes


def jarvis_init():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        hour = "Good Morning Sir !"
    elif hour >= 12 and hour < 18:
        hour = "Good Afternoon Sir !"
    else:
        hour = "Good Evening Sir !"
    time = dateAndTime("current_time")
    respond = hour + " currently its " + time + ",Initialising JARVIS PROGRAM... Always at your service"
    speak(respond)
    main()


def speak(text):
    tts = gTTS(text=text, lang='en-us')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove("voice.mp3")


def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            pass

    return said.lower()


def dateAndTime(type):
    if type == "current_time":
        now = datetime.now()
        date = now.strftime("%H:%M %p")
        date = str(date)
    elif type == "current_date":
        now = datetime.now()
        date = now.strftime("%d/%m/%y")
        date = str(date)

    return date


def getRespond(command):
    print("User: ", command)
    if "thank you" in command:
        random_respond = random.choice(["No problem sir", "I am always here for you", "Any time sir."])
        speak(random_respond)
    elif "what date is today" in command:
        now = dateAndTime("current_date")
        print(now)
        speak(now)
    elif "what time is it" in command:
        now = dateAndTime("current_time")
        speak(now)
    elif "search google for" in command:
        args = command.split("search google for")
        search = args[1]
        if search != "":
            url = "https://www.google.com/search?q=" + search
            respond = "Do you wan't me to search " + search + " in google?"
            speak(respond)
            yes_no = getAudio()
            if "yes" in yes_no:
                webbrowser.open(url)
            if "no" in yes_no:
                speak("Alright sir, no problem.")
        elif search == "":
            speak("Sorry sir, but i didn't catch the last part, can you repeat what do you want me to search google "
                  "for?")
            audio = getAudio()
            respond = "Do you want me to search google for " + audio
            url = "https://www.google.com/search?q=" + audio
            speak(respond)
            yes_no = getAudio()
            if "yes" in yes_no:
                webbrowser.open(url)
            if "no" in yes_no:
                speak("Alright sir, no problem.")
    elif "take me to" in command:

        search = command.split("")
        if search != "":
            respond = "Do you wan't me to take you to " + search
            speak(respond)
            yes_no = getAudio()
            if yes_no == "no":
                speak("Alright sir.")
            elif yes_no == "yes":
                respond = "I'm taking you to " + search
                speak(respond)
                url = "https://www.google.co.uk/maps/dir//" + search
                webbrowser.open(url)
        if search == "":
            speak("Where do you want to go?")
            audio = getAudio()
            if audio != None:
                respond = "Do you wan't me to take you to " + audio
                speak(respond)
                yes_no = getAudio()
                if yes_no == "no":
                    speak("Alright sir.")
                elif yes_no == "yes":
                    respond = "I'm taking you to " + audio
                    speak(respond)
                    url = "https://www.google.co.uk/maps/dir//" + audio
                    webbrowser.open(url)
    elif "search youtube for" in command:
        args = command.split("search youtube for")
        search = args[1]
        if search != "":
            audio = getAudio()
            respond = "I'm on it... Searching youtube for " + audio
            speak(respond)
            url = "https://www.youtube.com/results?search_query=" + audio
            webbrowser.open(url)
        if search == "":
            speak("Sorry sir, but i didn't catch the last part, can you repeat what do you want me to search youtube "
                  "for?")
            audio = getAudio()
            respond = "Do you want me to search youtube for " + audio
            url = "https://www.youtube.com/results?search_query=" + audio
            speak(respond)
            yes_no = getAudio()
            if "yes" in yes_no:
                webbrowser.open(url)
            if "no" in yes_no:
                speak("Alright sir, no problem.")
    elif "make note" in command:
        speak("What do you want to write in your notes?")
        getNote = getAudio()
        if getNote != "":
            respond = "Your note: " + getNote
            speak(respond)
            speak("Do you want to save it?")

            yes_no = getAudio()
            if "yes" in yes_no:
                file = open('jarvis.txt', 'w')
                now = datetime.now()
                date = now.strftime("%d/%m/%y %H:%M %p")
                file.write(date)
                file.write(" :- ")
                file.write(getNote)
                speak("Note has been created")
            elif "no" in yes_no:
                speak("Alright, I will not make any notes.")
        else:
            speak("Sorry sir, to make a note you have to write something.")
    elif "read notes" in command or "raed my notes" in command:
        file = open('jarvis.txt', 'r')
        content = file.read()
        speak("Yes sir, those are yours notes.")
        speak(content)
    elif "delete my notes" in command or "delete notes" in command:
        speak("Are you sure you want me to delete your notes?")
        yes_no = getAudio()
        if "yes" in yes_no or "sure" in yes_no:
            os.remove('jarvis.txt')
            speak("Your notes has been deleted.")
        elif "no" in yes_no:
            speak("Close one? I will not delete your notes.")
    elif "solve" in command or "calculate" in command:
        if "solve" in command:
            args = command.split("solve")
        if "calculate" in command:
            args = command.split("calculate")
        if args[1] != "":
            equation = "{}".format(args[1]).lower()
            orginal = args[1]
            equation = equation.replace(" x ", " * ")
            ans = eval(equation)
            respond = f"{orginal} is equal to {ans}"
            print(respond)
            speak(respond)
        else:
            speak("I'm sorry sir, but you can't calculate nothing.")

    # QUESTIONS and casual resposes
    elif "tell me a joke" in command:
        speak(pyjokes.get_joke())
    elif "who are you" in command:
        speak("I am Just A Rather Very Intelligent System, but you can call me Jarvis")
    elif "who created you" in command:
        speak("My creator is Bartosz Szczepkowski")

    else:
        speak("Sorry sir, but i cannot find this command in my database, perhaps you can program one.")


def main():
    while True:
        wake_word = ["hey jarvis", "jarvis time to wake up"]
        respond = ["Always for your service sir", "Yes sir!", "Always here"]
        print("System log: Waiting for wake up.")
        audio = getAudio()
        if audio in wake_word:
            playsound.playsound('wake.mp3')
            ran_respond = random.choice(respond)
            speak(ran_respond)
            print("System log: Waiting for command")
            audio = getAudio()
            getRespond(audio)


if __name__ == "__main__":
    jarvis_init()
