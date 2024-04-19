import pyttsx3
import speech_recognition as sr
import datetime  # Import datetime module
import webbrowser
import subprocess

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour  # Accessing datetime module
    if 0 <= hour < 12:
        speak("Good Morning Sir,")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("I am Jarvis. Please tell me how can I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        speak("Sorry Sir, please say that again")
        return "None"

    return query


def get_system_weather():
    try:
        # Use curl command to fetch weather data from wttr.in service
        weather_data = subprocess.check_output(["curl", "wttr.in"])
        return weather_data.decode("utf-8")
    except Exception as e:
        return f"Error retrieving weather data: {str(e)}"


def extract_temperature(weather_data):
    # Extract temperature from weather data
    lines = weather_data.splitlines()
    temperature_line = lines[0]
    temperature = temperature_line.split()[0]  # Extract temperature value
    return temperature
def extract_basic_weather_condition(weather_data):
    # Extract basic weather condition from weather data
    lines = weather_data.splitlines()
    weather_condition_line = lines[2]
    if 'Sunny' in weather_condition_line:
        return 'sunny'
    elif 'Cloudy' in weather_condition_line:
        return 'cloudy'
    elif 'Rain' in weather_condition_line:
        return 'rainy'
    elif 'Snow' in weather_condition_line:
        return 'snowy'
    else:
        return 'unknown'




if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/?gl=IN&tab=r1")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'what can you do' in query:
            speak('I can open google, open youtube, tell time, tell weather')

        if 'weather' in query:
            weather_info = get_system_weather()
            temperature = extract_temperature(weather_info)
            basic_weather_condition = extract_basic_weather_condition(weather_info)
            speak(f"The weather is {basic_weather_condition}. The temperature is {temperature} degrees Celsius.")


        elif 'exit' in query:
            speak("Have a good day sir, bye")
            exit()
