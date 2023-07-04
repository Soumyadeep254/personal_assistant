import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import getpass
import os
import smtplib
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    username = getpass.getuser()
    speak("Hi " + username + ", I am your personal assistant. How may I help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Please repeat that...")
        return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()

    jokes = [
        "Did you hear about the guy whose whole left side was cut off? He's all right now.",
        "I'm reading a book about anti-gravity. It's impossible to put down.",
        "I wondered why the baseball was getting bigger. Then it hit me.",
        # Add more jokes here...
    ]

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'set timer for' in query:
            import time
            query = query.replace("set timer for ", "")
            query = int(query.replace("mins", ""))
            mins = 1
            print("Running Time for {}".format(query))
            while mins != query + 1:
                print("{}".format(mins))
                time.sleep(60)
                mins += 1

        elif 'search google' in query:
            speak('Searching Google...')
            query = query.replace("google", "")
            for j in search(query, tld="co.in", num=10, stop=10, pause=2):
                print(j)

        elif "joke" in query:
            joke = random.choice(jokes)
            print(joke)
            speak(joke)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open github' in query:
            webbrowser.open("github.com")

        elif 'open' in query:
            # Add code to handle opening specific applications or websites
            pass

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "recipient@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email at the moment.")

        elif 'quit' in query:
            speak("Goodbye!")
            exit()

