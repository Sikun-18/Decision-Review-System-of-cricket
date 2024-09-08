import tkinter  # Import the tkinter library for GUI development
import cv2  # Import the OpenCV library for video processing
import PIL.Image, PIL.ImageTk  # Import the PIL library for handling images
from functools import partial  # Import partial for passing arguments to functions
import threading  # Import threading to handle concurrent execution
import imutils  # Import imutils for image processing and resizing
import time  # Import time for adding delays
import speech_recognition as sr  # Import the speech recognition library for voice commands
import pyttsx3  # Import the pyttsx3 library for text-to-speech

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Load the video file
stream = cv2.VideoCapture("runout.mp4")

def play(speed):
    print(f"You clicked on play. Speed is {speed}")
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()
    
    if not grabbed:
        stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
        grabbed, frame = stream.read()
    
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

def pending(decision):
    frame = cv2.cvtColor(cv2.imread("decision_pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    time.sleep(1)
    
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    time.sleep(1.5)
    
    decisionImg = "out.png" if decision == "out" else "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    
    # Speak the decision
    engine.say(f"The player is {decision}")
    engine.runAndWait()

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized command: {command}")
        
        if "play fast" in command:
            play(25)
        elif "play slow" in command:
            play(2)
        elif "reverse fast" in command:
            play(-25)
        elif "reverse slow" in command:
            play(-2)
        elif "out" in command:
            out()
        elif "not out" in command:
            not_out()
        else:
            print("Command not recognized.")
    
    except sr.UnknownValueError:
        print("Sorry, I did not understand the command.")
    except sr.RequestError:
        print("Could not request results; check your network connection.")

def start_listening():
    while True:
        recognize_speech()

# Width and height of our main screen
SET_WIDTH = 733
SET_HEIGHT = 400

# Tkinter GUI starts here
window = tkinter.Tk()
window.title("Decision Review Kit")
cv_img = cv2.cvtColor(cv2.imread("drs.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous(fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous(slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next(fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Next(slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()

# Start a separate thread for voice command listening
voice_thread = threading.Thread(target=start_listening)
voice_thread.daemon = True
voice_thread.start()

# Start the Tkinter event loop
window.mainloop()
