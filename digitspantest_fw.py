import tkinter as tk
import random
import string
import speech_recognition as sr
from PIL import Image, ImageTk
import os
import time

motivational_lines = [
    "You're doing great! Keep it up!",
    "Amazing memory power!",
    "Impressive! Stay focused!",
    "You're on fire today!",
    "Fantastic! You're crushing it!",
    "Great job! Let's keep the streak going!",
    "Sharp mind! Ready for the next one?",
    "Brain training master in action!"
]

docs = "\nClick 'Start' or press 'Enter' if you are ready to start the test."
title = 'Digit Span Test for Memory Evaluation'

sequence_store = {}

def startTest(mode):
    def runTest(*args):
        global i, DIGITS, FAILURES, SCORE, paused, start_time, total_test_start_time, consecutive_correct, current_level
        wdw.unbind('<Return>')
        canvas.delete('all')

        if total_test_start_time == 0:
            total_test_start_time = time.time()

        nums = ['Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven',
                'Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen']

        i += 1
        counter = i - 1

        if SCORE < 0:
            i = 0
            DIGITS = 3
            FAILURES = 0
            SCORE = 0
            consecutive_correct = 0
            current_level = 1
            runTest()
            return

        # New level progression logic: increase level after 2 consecutive correct answers
        if consecutive_correct >= 2:
            current_level += 1
            DIGITS += 1
            consecutive_correct = 0  # Reset counter after level increase
        
        # Ensure minimum digit count
        DIGITS = max(3, DIGITS)

        # Reverse input required after level 3 (when DIGITS >= 6)
        reverse_required = current_level > 3

        txt = '{0}-Character Sequence (Level {1})'.format(nums[min(DIGITS-3, len(nums)-1)], current_level)
        instruction = "Type the **REVERSED** sequence" if reverse_required else "Type the sequence normally"

        seqtxt = canvas.create_text(Width/2, Height/3.5, fill='darkblue', 
                                     font='Arial 32', text=txt, justify='c')
        canvas.create_text(Width/2, Height/3, fill='red', font='Arial 24', text=instruction)

        # Display level and consecutive correct info
        level_info = f'Level: {current_level} | Consecutive: {consecutive_correct}/2'
        canvas.create_text(Width - 200, 80, fill='purple', 
                          font='Arial 18 bold', text=level_info, tags='level_info')

        score_text = canvas.create_text(Width - 150, 50, fill='darkgreen', 
                                        font='Arial 20 bold', text=f'Score: {SCORE}', tags='score')

        canvas.after(1200, canvas.update())

        if mode == 'number':
            seq = random.sample(range(10), min(DIGITS, 10))  # Ensure we don't exceed available digits
            while not isValidSequence(seq):
                seq = random.sample(range(10), min(DIGITS, 10))
            seq_digits = ''.join(str(d) for d in seq)
        else:
            seq = random.sample(string.ascii_uppercase, min(DIGITS, 26))  # Ensure we don't exceed available letters
            while not isValidSequenceAlpha(seq):
                seq = random.sample(string.ascii_uppercase, min(DIGITS, 26))
            seq_digits = ''.join(seq)

        sequence_store['current'] = seq_digits
        sequence_store['reverse'] = reverse_required

        canvas.delete('all')
        # Show sequence with a slight delay between characters
        for a in range(len(seq_digits)):
            if paused:
                return
            z = canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                   font='Times 160', text=seq_digits[a], justify='c')
            canvas.after(1000, canvas.update())
            canvas.delete(z)
            # Small pause between digits
            canvas.after(200, canvas.update())

        label = canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Repeat the sequence here', justify='c')
        
        # Show instruction again
        instruction_reminder = "Enter REVERSED sequence" if reverse_required else "Enter sequence normally"
        canvas.create_text(Width/2, Height/2.1, fill='red', 
                          font='Arial 20', text=instruction_reminder, justify='c')

        entry_width = max(3, len(seq_digits))
        entry = tk.Text(wdw, width=entry_width, height=1, font=('Arial', 32))
        e = canvas.create_window(Width/2, Height/2, window=entry)
        entry.focus()

        start_time = time.time()

        def delete():
            canvas.delete('all')
            runTest()

        def stop_game():
            global userNumbers, generatedNumbers
            total_time = time.time() - total_test_start_time
            canvas.delete('all')
            canvas.create_text(Width/2, Height/4, fill='darkblue', 
                               font='Arial 36', text='Game Over. Here are your results:', justify='c')
            canvas.create_text(Width/2, Height/2.8, fill='darkblue', 
                               font='Arial 28', text=f'Total Score: {SCORE}', justify='c')
            canvas.create_text(Width/2, Height/2.5, fill='purple', 
                               font='Arial 24', text=f'Highest Level Reached: {current_level}', justify='c')
            canvas.create_text(Width/2, Height/2.2, fill='darkgreen', 
                               font='Arial 20', text=f'Entries: {len(userNumbers)} | Total Time: {int(total_time)} seconds', justify='c')
            canvas.create_text(Width/2, Height/1.9, fill='blue', 
                               font='Arial 20 italic', text=random.choice(motivational_lines), justify='c')
            
            # Enhanced attention level calculation
            if current_level >= 5:
                attention_level = 'Excellent'
            elif current_level >= 4:
                attention_level = 'High'
            elif current_level >= 3:
                attention_level = 'Good'
            elif current_level >= 2:
                attention_level = 'Moderate'
            else:
                attention_level = 'Needs Improvement'
                
            canvas.create_text(Width/2, Height/1.6, fill='orange', 
                               font='Arial 24', text=f'Attention Level: {attention_level}', justify='c')

        def get_text(event=None):
            global userNumbers, generatedNumbers, FAILURES, i, DIGITS, SCORE, consecutive_correct
            content = entry.get(1.0, "end-1c").upper().replace(" ", "")
            expected = sequence_store['current'][::-1] if sequence_store['reverse'] else sequence_store['current']
            userNumbers.append(content)
            generatedNumbers.append(sequence_store['current'] + (" (reversed)" if sequence_store['reverse'] else " (normal)"))

            canvas.delete("all")

            if content == expected:
                SCORE += 1
                consecutive_correct += 1  # Increment consecutive correct counter
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Correct! Continue...', justify='c')
                
                # Show progress towards next level
                if consecutive_correct < 2:
                    progress_text = f"Consecutive correct: {consecutive_correct}/2 - Keep going!"
                    canvas.create_text(Width/2, Height/2, fill='orange', 
                                      font='Arial 18', text=progress_text)
                else:
                    level_up_text = f"Level up! Moving to Level {current_level + 1}"
                    canvas.create_text(Width/2, Height/2, fill='purple', 
                                      font='Arial 20 bold', text=level_up_text)
                
                motivation = random.choice(motivational_lines)
                canvas.create_text(Width/2, Height/1.6, fill='green', 
                                   font='Arial 20 italic', text=motivation)
                canvas.after(2000, delete)  # Slightly longer delay to show level progress
            else:
                SCORE -= 2
                consecutive_correct = 0  # Reset consecutive counter on wrong answer
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Incorrect! Try again!', justify='c')
                canvas.create_text(Width/2, Height/2, fill='red', 
                                  font='Arial 18', text='Consecutive progress reset', justify='c')
                FAILURES += 1
                if FAILURES < 3:
                    i -= 1
                    canvas.after(1500, delete)
                else:
                    stop_game()

        def repeat_sequence():
            global SCORE, consecutive_correct
            SCORE -= 2
            consecutive_correct = 0  # Reset consecutive counter when using repeat
            canvas.delete('all')
            canvas.create_text(Width/2, Height/3, fill='orange', 
                              font='Arial 20', text='Repeating sequence (consecutive progress reset)', justify='c')
            canvas.after(1000, canvas.update())
            
            for a in range(len(sequence_store['current'])):
                z = canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                       font='Times 160', text=sequence_store['current'][a], justify='c')
                canvas.after(1000, canvas.update())
                canvas.delete(z)
                canvas.after(200, canvas.update())
            runTest()

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

        def toggle_pause():
            global paused
            paused = not paused
            if paused:
                canvas.create_text(Width/2, Height/1.1, fill='red', font='Arial 20 bold', text='Paused', tag='pause_msg')
            else:
                canvas.delete('pause_msg')
                runTest()

        entry.bind('<Return>', get_text)

        button_continue = tk.Button(wdw, height=2, width=10, text='Continue', 
                                    font='Arial 20', fg='black', command=get_text, bd=0)
        button_continue.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
        canvas.create_window(Width/2, Height/1.5, window=button_continue)

        speak_btn = tk.Button(wdw, height=2, width=10, text='Speak',
                              font='Arial 20', fg='black', command=recognize_speech, bd=0)
        speak_btn.configure(bg='#20B2AA', activebackground='#2E8B57', activeforeground='white')
        canvas.create_window(Width/2, Height/1.35, window=speak_btn)

        repeat_btn = tk.Button(wdw, height=2, width=25, text='Repeat Sequence (-2 & Reset)',
                               font='Arial 16', fg='black', command=repeat_sequence, bd=0)
        repeat_btn.configure(bg='#FF8C00', activebackground='#FF4500', activeforeground='white')
        canvas.create_window(Width/2, Height/1.2, window=repeat_btn)

        pause_btn = tk.Button(wdw, height=2, width=10, text='Pause',
                              font='Arial 16', fg='black', command=toggle_pause, bd=0)
        pause_btn.configure(bg='#B0C4DE', activebackground='#708090', activeforeground='white')
        canvas.create_window(Width - 240, Height - 80, window=pause_btn)

        stop_btn = tk.Button(wdw, height=2, width=10, text='Stop Game',
                             font='Arial 16', fg='black', command=stop_game, bd=0)
        stop_btn.configure(bg='#DC143C', activebackground='#8B0000', activeforeground='white')
        canvas.create_window(Width - 120, Height - 80, window=stop_btn)

    runTest()

def isValidSequence(seq):
    if len(seq) <= 1:
        return True
    for x in range(len(seq)-1):
        if abs(seq[x] - seq[x+1]) == 1:
            return False
    return True

def isValidSequenceAlpha(seq):
    if len(seq) <= 1:
        return True
    for x in range(len(seq)-1):
        if abs(ord(seq[x]) - ord(seq[x+1])) == 1:
            return False
    return True

wdw = tk.Tk()
wdw.title('Enhanced Digit Span Test')
Width = wdw.winfo_screenwidth()
Height = wdw.winfo_screenheight()
wdw.geometry("%dx%d" % (Width, Height))
canvas = tk.Canvas(wdw, bg='#FDF5E6')
canvas.pack(fill='both', expand=True)
wdw.state('zoomed')

canvas.create_text(Width/2, Height/4.5, fill='darkblue', 
                   font='Arial 52', text=title, justify='c')
canvas.create_text(Width/2, Height/2.4, fill='darkblue', 
                   font='Arial 28', text='New Features:', justify='c')
canvas.create_text(Width/2, Height/2.1, fill='darkgreen', 
                   font='Arial 20', text='• Level up after 2 consecutive correct answers', justify='c')
canvas.create_text(Width/2, Height/1.95, fill='darkgreen', 
                   font='Arial 20', text='• Reverse input required after Level 3', justify='c')
canvas.create_text(Width/2, Height/1.8, fill='darkblue', 
                   font='Arial 24', text=docs, justify='c')

# Initialize new global variables
i = 0
DIGITS = 3  # Start with 3 digits
FAILURES = 0
SCORE = 0
paused = False
consecutive_correct = 0  # Track consecutive correct answers
current_level = 1  # Track current level
userNumbers, generatedNumbers = [], []
start_time = 0
total_test_start_time = 0

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