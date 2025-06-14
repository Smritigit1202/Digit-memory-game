import tkinter as tk     
import random
import string
import speech_recognition as sr  # <-- New Import
from PIL import Image, ImageTk  # <-- For Avatar feature
import os

# Load avatar image
AVATAR_PATH = "avatar_happy.png"  # Make sure this image is in the same folder
avatar_img = None
if os.path.exists(AVATAR_PATH):
    avatar_raw = Image.open(AVATAR_PATH).resize((150, 150))
    avatar_img = ImageTk.PhotoImage(avatar_raw)

# Motivational messages
motivational_lines = [
    "You're doing great! Keep it up!",
    "Amazing memory power!",
    "Impressive! Stay focused!",
    "You're on fire today!",
    "Fantastic! You're crushing it!",
    "Great job! Let’s keep the streak going!",
    "Sharp mind! Ready for the next one?",
    "Brain training master in action!"
]

docs = '''\nClick 'Start' or press 'Enter' if you are ready to start the test.'''
title = 'Digit Span Test for Memory Evaluation'

def startTest(mode):
    def runTest(*args):
        global i, DIGITS, FAILURES
        wdw.unbind('<Return>')
        canvas.delete('all')

        nums = ['Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven',
                'Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen']

        DIGITS += 1
        i += 1
        counter = i - 1

        reverse_required = DIGITS >= 5 and (DIGITS % 2 == 1)

        txt = '{0}-Character Sequence'.format(nums[i-1])
        instruction = "Type the **REVERSED** sequence" if reverse_required else "Type the sequence normally"

        seqtxt = canvas.create_text(Width/2, Height/3.5, fill='darkblue', 
                                     font='Arial 32', text=txt, justify='c')
        canvas.create_text(Width/2, Height/3, fill='red', font='Arial 24', text=instruction)

        canvas.after(1200, canvas.update())

        if mode == 'number':
            seq = random.sample(range(10), DIGITS)
            while not isValidSequence(seq):
                seq = random.sample(range(10), DIGITS)
            seq_digits = ''.join(str(d) for d in seq)
        else:
            seq = random.sample(string.ascii_uppercase, DIGITS)
            while not isValidSequenceAlpha(seq):
                seq = random.sample(string.ascii_uppercase, DIGITS)
            seq_digits = ''.join(seq)

        for a in range(len(seq_digits)):
            z = canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                   font='Times 160', text=seq_digits[a], justify='c')
            canvas.after(1000, canvas.update())
            canvas.delete(z)        

        label = canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Repeat the sequence here', justify='c')

        entry_width = max(5, min(25, len(seq_digits) + 2))
        entry = tk.Text(wdw, width=entry_width, height=1, font=('Arial', 32))
        e = canvas.create_window(Width/2, Height/2, window=entry)
        entry.focus()

        def delete():
            canvas.delete('all')
            runTest()

        def get_text(event=None):
            global userNumbers, generatedNumbers, FAILURES, i, DIGITS
            content = entry.get(1.0, "end-1c").upper().replace(" ", "")
            expected = seq_digits[::-1] if reverse_required else seq_digits
            userNumbers.append(content)
            generatedNumbers.append(seq_digits if not reverse_required else seq_digits + " (reversed)")

            canvas.delete(label, b, e, seqtxt, speak_button)
            canvas.delete("avatar")

            if content == expected:
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Correct! Continue...', justify='c')
                if avatar_img:
                    canvas.create_image(Width/2, Height/1.8, image=avatar_img, tags="avatar")
                motivation = random.choice(motivational_lines)
                canvas.create_text(Width/2, Height/1.6, fill='green', 
                                   font='Arial 20 italic', text=motivation, tags="avatar")
                canvas.after(1500, delete)
            else:
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Try again!', justify='c')
                FAILURES += 1
                if FAILURES < 3:
                    i -= 1
                    DIGITS -= 1
                    canvas.after(1200, delete)
                else:
                    canvas.delete('all')
                    canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                       font='Arial 26', text='Thank you for your participation!', justify='c')
                    canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                       font='Arial 36', text='Your score: {0}'.format(counter), justify='c')
                    wdw.after(3000, lambda: wdw.destroy())

        def recognize_speech():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                canvas.create_text(Width/2, Height/1.8, fill='green', 
                                   font='Arial 20', text='Listening...', tag='listen_msg')
                wdw.update()
                try:
                    audio = r.listen(source, timeout=5)
                    canvas.delete('listen_msg')
                    text = r.recognize_google(audio)
                    cleaned = ''.join(c for c in text if c.isalnum()).upper()
                    entry.delete(1.0, 'end')
                    entry.insert('end', cleaned)
                except sr.UnknownValueError:
                    canvas.delete('listen_msg')
                    canvas.create_text(Width/2, Height/1.8, fill='red', 
                                       font='Arial 20', text='Could not understand. Try again.', tag='listen_msg')
                except sr.RequestError:
                    canvas.delete('listen_msg')
                    canvas.create_text(Width/2, Height/1.8, fill='red', 
                                       font='Arial 20', text='Speech service failed.', tag='listen_msg')

        button2 = tk.Button(wdw, height=2, width=10, text='Continue', 
                            font='Arial 20', fg='black', command=get_text, bd=0)
        button2.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
        entry.bind('<Return>', get_text)  
        b = canvas.create_window(Width/2, Height/1.6, window=button2)

        speak_btn = tk.Button(wdw, height=2, width=10, text='Speak',
                              font='Arial 20', fg='black', command=recognize_speech, bd=0)
        speak_btn.configure(bg='#20B2AA', activebackground='#2E8B57', activeforeground='white')
        speak_button = canvas.create_window(Width/2, Height/1.4, window=speak_btn)

    runTest()

def isValidSequence(seq):
    for x in range(len(seq)-1):
        if abs(seq[x] - seq[x+1]) == 1:
            return False
    return True

def isValidSequenceAlpha(seq):
    for x in range(len(seq)-1):
        if abs(ord(seq[x]) - ord(seq[x+1])) == 1:
            return False
    return True

wdw = tk.Tk()
wdw.title('Digit Span Test')
Width = wdw.winfo_screenwidth()
Height = wdw.winfo_screenheight()
wdw.geometry("%dx%d" % (Width, Height))
canvas = tk.Canvas(wdw, bg='#FDF5E6')
canvas.pack(fill='both', expand=True)
wdw.state('zoomed')

canvas.create_text(Width/2, Height/4.5, fill='darkblue', 
                   font='Arial 52', text=title, justify='c')
canvas.create_text(Width/2, Height/2.2, fill='darkblue', 
                   font='Arial 36', text=docs, justify='c')

i = 0
DIGITS = 2
FAILURES = 0
userNumbers, generatedNumbers = [], []

button_num = tk.Button(wdw, height=2, width=10, text='Numbers', 
                       font='Arial 24', fg='black', command=lambda: startTest('number'), bd=0)
button_num.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
canvas.create_window(Width/2 - 150, Height/1.4, window=button_num)

button_alpha = tk.Button(wdw, height=2, width=10, text='Alphabets', 
                         font='Arial 24', fg='black', command=lambda: startTest('alphabet'), bd=0)
button_alpha.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
canvas.create_window(Width/2 + 150, Height/1.4, window=button_alpha)

wdw.mainloop()

print('Generated: ', generatedNumbers)
print('Repeated:  ', userNumbers)