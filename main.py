import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import openai
import datetime
import random
import pywhatkit as kit
from  config  import apikey






# Text-to-speech setup
voice_jarvis = pyttsx3.init("sapi5")
voice_jarvis.setProperty('rate', 140)
voice_jarvis.setProperty('volume', 2)
voices = voice_jarvis.getProperty('voices')
voice_jarvis.setProperty('voice', voices[0].id)


# OpenAI key and base setup
from openai import OpenAI, api_key

# Use OpenRouter as the API base
client = OpenAI(
    api_key=apikey,
    base_url="https://openrouter.ai/api/v1"
)

conversation = []

def chat_with_memory(user_input):
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openchat/openchat-3.5-0106",
        messages=conversation,
        temperature=0.7,
        max_tokens=300
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return reply

def ai(prompt):
    openai.api_key = "apikey"
    openai.api_base = "https://openrouter.ai/api/v1"
    text = f"open ai response for prompt: {prompt}\n*******\n\n"
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    text += response["choices"][0]["text"]
    print(response["choices"][0]["text"])
    if not os.path.exists("openai files"):
        os.mkdir("openai files")
    with open(f"openai files/prompts-{random.randint(1, 850)}.txt", "w") as f:
        f.write(text)
    return text

def cahat_ai(query):
    print(query)
    conversation.append({"role": "user", "content": query})
    response = openai.ChatCompletion.create(
        model="openchat/openchat-3.5-0106",
        messages=conversation,
        temperature=0.7,
        max_tokens=300
    )
    reply = response["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": reply})
    return reply

def whatsappmesege(contact_number, mesege):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 2

    try:
        say(f"sending whatsappmesege to {contact_number}")
        kit.sendwhatmsg(contact_number, mesege, hour, minute)
    except Exception as e:
        say("sorry sir, message is not sent due to some issue")
        print(f"error: {e}")

def say(text):
    voice_jarvis.say(text)
    voice_jarvis.runAndWait()

def takecomand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        r.phrase_threshold=0.3
        r.energy_threshold=300
        r.dynamic_energy_threshold=True
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query=r.recognize_google(audio, language='en-ind')
            print(f"user said: {query}")
            return query
        except Exception as e:
            print("error mila hai sir ",e)
            say("error mila hai sir")
            say(str(e))
            return "sorry sir"
if __name__ == '__main__':
    print('PyCharm running...')
    say("HEY, I am Friday!")

    while True:
        print("Listening...")
        query = takecomand()

        # Open websites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["w3school", "https://www.w3schools.com/"],
            ["google", "https://www.google.com"]
        ]
        for site in sites:
            if "open" in query.lower() and site[0] in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # Play music
        if "music" in query.lower():
            musicpath = r"C:\Users\USER\Downloads\gorila-315977.mp3"
            say("Playing music sir...")
            os.startfile(musicpath)

        # Time
        if "time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minit = datetime.datetime.now().strftime("%M")
            say(f"Sir, time is {hour} bajjkar {minit} minutes")

        # for openings app
        apps = [["notepad", "notepad"],["netflix", "start shell:AppsFolder\\4DF9E0F8.Netflix_mcm4njqhnhss8!Netflix.App"],["paint","mspaint"],["calculator","calc"]]
        for app in apps:
           if "open" in query.lower() and app[0] in query.lower():
                say(f"opening {app[0]} sir....")
                os.system(app[1])

        # WhatsApp messaging block
        if "whatsap" in query.lower():
            say("Please tell me the contact name.")
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 2

            name = takecomand().lower()

            contacts = {
                "mummy": "+917014869775",
                "dad": "+919509123001",
                "bestie": "+919876543210"
            }


            name_real= takecomand().lower()

            if name_real!="sory sir" and name_real in contacts:
                say(f"did you mean {"name_real"}")


            confirm=takecomand().lower()
            if "yes" in confirm.lower() or "y" in confirm.lower():
                say("what should you send ")
                msg = takecomand()
                whatsappmesege(contacts.get(name, name), msg)
            if "stop" in name:
                say("ok boss quiting the process")
                break
            else:
                say("sory sir i  cant send meseage")






        # Conversation mode block
        if "conversation" in query:
            say("Friday conversation mode on. Ask me anything.")
            while True:
                user_input = takecomand()
                if "stop" in user_input:
                    say("Okay boss, exiting conversation mode.")
                    break
                if user_input.strip() == "":
                    continue
                response = chat_with_memory(user_input)
                print(f" Friday: {response}")
                say(response)

else:
    say("work is not done")






