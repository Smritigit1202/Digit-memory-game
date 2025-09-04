import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import speech_recognition as sr
from PIL import Image, ImageTk
import os
import time
import json
from datetime import datetime

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
LEADERBOARD_FILE = 'digit_span_leaderboard.json'

# Leaderboard functions
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

def add_to_leaderboard(player_name, score, level, mode, total_time):
    leaderboard = load_leaderboard()
    entry = {
        'name': player_name,
        'score': score,
        'level': level,
        'mode': mode,
        'time': total_time,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    leaderboard.append(entry)
    # Sort by score (descending), then by level (descending)
    leaderboard.sort(key=lambda x: (x['score'], x['level']), reverse=True)
    # Keep only top 20 scores
    leaderboard = leaderboard[:20]
    save_leaderboard(leaderboard)
    return leaderboard

def show_leaderboard():
    leaderboard = load_leaderboard()
    canvas.delete('all')
    
    # Title
    canvas.create_text(Width/2, 80, fill='darkblue', 
                       font='Arial 36 bold', text='🏆 LEADERBOARD 🏆', justify='center')
    
    if not leaderboard:
        canvas.create_text(Width/2, Height/2, fill='red', 
                           font='Arial 24', text='No scores yet! Be the first to play!', justify='center')
    else:
        # Headers
        y_start = 150
        canvas.create_text(150, y_start, fill='purple', font='Arial 18 bold', text='RANK', justify='center')
        canvas.create_text(300, y_start, fill='purple', font='Arial 18 bold', text='NAME', justify='center')
        canvas.create_text(450, y_start, fill='purple', font='Arial 18 bold', text='SCORE', justify='center')
        canvas.create_text(600, y_start, fill='purple', font='Arial 18 bold', text='LEVEL', justify='center')
        canvas.create_text(750, y_start, fill='purple', font='Arial 18 bold', text='MODE', justify='center')
        canvas.create_text(900, y_start, fill='purple', font='Arial 18 bold', text='TIME', justify='center')
        canvas.create_text(1100, y_start, fill='purple', font='Arial 18 bold', text='DATE', justify='center')
        
        # Draw line under headers
        canvas.create_line(50, y_start + 20, Width - 50, y_start + 20, fill='purple', width=2)
        
        # Display entries
        for i, entry in enumerate(leaderboard[:15]):  # Show top 15
            y_pos = y_start + 50 + (i * 35)
            
            # Color coding for top 3
            if i == 0:
                color = '#FFD700'  # Gold
                rank_text = '🥇 1st'
            elif i == 1:
                color = '#C0C0C0'  # Silver
                rank_text = '🥈 2nd'
            elif i == 2:
                color = '#CD7F32'  # Bronze
                rank_text = '🥉 3rd'
            else:
                color = 'darkblue'
                rank_text = f'{i+1}'
            
            canvas.create_text(150, y_pos, fill=color, font='Arial 16 bold', text=rank_text, justify='center')
            canvas.create_text(300, y_pos, fill=color, font='Arial 16', text=entry['name'][:12], justify='center')
            canvas.create_text(450, y_pos, fill=color, font='Arial 16 bold', text=str(entry['score']), justify='center')
            canvas.create_text(600, y_pos, fill=color, font='Arial 16', text=str(entry['level']), justify='center')
            canvas.create_text(750, y_pos, fill=color, font='Arial 16', text=entry['mode'].title(), justify='center')
            canvas.create_text(900, y_pos, fill=color, font='Arial 16', text=f"{entry['time']}s", justify='center')
            canvas.create_text(1100, y_pos, fill=color, font='Arial 14', text=entry['date'][:10], justify='center')
    
    # Statistics
    if leaderboard:
        stats_y = Height - 200
        canvas.create_text(Width/2, stats_y, fill='darkgreen', font='Arial 20 bold', text='STATISTICS', justify='center')
        
        total_games = len(leaderboard)
        avg_score = sum(entry['score'] for entry in leaderboard) / total_games
        highest_level = max(entry['level'] for entry in leaderboard)
        
        canvas.create_text(Width/2, stats_y + 30, fill='darkgreen', font='Arial 16', 
                          text=f'Total Games Played: {total_games} | Average Score: {avg_score:.1f} | Highest Level: {highest_level}', 
                          justify='center')
    
    # Back button
    back_btn = tk.Button(wdw, height=2, width=15, text='Back to Menu', 
                         font='Arial 18', fg='white', command=show_main_menu, bd=0)
    back_btn.configure(bg='#4682B4', activebackground='#36648B')
    canvas.create_window(Width/2, Height - 100, window=back_btn)
    
    # Export button
    export_btn = tk.Button(wdw, height=2, width=15, text='Export to CSV', 
                           font='Arial 18', fg='white', command=export_leaderboard, bd=0)
    export_btn.configure(bg='#228B22', activebackground='#006400')
    canvas.create_window(Width/2 - 200, Height - 100, window=export_btn)

def export_leaderboard():
    leaderboard = load_leaderboard()
    if not leaderboard:
        messagebox.showinfo("Export", "No data to export!")
        return
    
    try:
        import csv
        filename = f'digit_span_leaderboard_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Rank', 'Name', 'Score', 'Level', 'Mode', 'Time (seconds)', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, entry in enumerate(leaderboard):
                writer.writerow({
                    'Rank': i + 1,
                    'Name': entry['name'],
                    'Score': entry['score'],
                    'Level': entry['level'],
                    'Mode': entry['mode'].title(),
                    'Time (seconds)': entry['time'],
                    'Date': entry['date']
                })
        
        messagebox.showinfo("Export Success", f"Leaderboard exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

def show_main_menu():
    canvas.delete('all')
    
    # Main title and info
    canvas.create_text(Width/2, Height/5, fill='darkblue', 
                       font='Arial 52', text=title, justify='center')
    canvas.create_text(Width/2, Height/2.8, fill='darkblue', 
                       font='Arial 28', text='New Features:', justify='center')
    canvas.create_text(Width/2, Height/2.5, fill='darkgreen', 
                       font='Arial 20', text='• Level up after 2 consecutive correct answers', justify='center')
    canvas.create_text(Width/2, Height/2.3, fill='darkgreen', 
                       font='Arial 20', text='• Reverse input required after Level 3', justify='center')
    canvas.create_text(Width/2, Height/2.1, fill='red', 
                       font='Arial 20', text='• Leaderboard system to track high scores', justify='center')
    canvas.create_text(Width/2, Height/1.9, fill='darkblue', 
                       font='Arial 24', text=docs, justify='center')
    
    # Start buttons
    button_num = tk.Button(wdw, height=3, width=15, text='Numbers', 
                           font='Arial 24', fg='black', command=lambda: startTest('number'), bd=0)
    button_num.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
    canvas.create_window(Width/2 - 200, Height - 200, window=button_num)
    
    button_alpha = tk.Button(wdw, height=3, width=15, text='Alphabets', 
                             font='Arial 24', fg='black', command=lambda: startTest('alphabet'), bd=0)
    button_alpha.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
    canvas.create_window(Width/2, Height - 200, window=button_alpha)
    
    # Leaderboard button
    leaderboard_btn = tk.Button(wdw, height=3, width=15, text='Leaderboard', 
                                font='Arial 24', fg='white', command=show_leaderboard, bd=0)
    leaderboard_btn.configure(bg='#FF8C00', activebackground='#FF4500')
    canvas.create_window(Width/2 + 200, Height - 200, window=leaderboard_btn)

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
                                     font='Arial 32', text=txt, justify='center')
        canvas.create_text(Width/2, Height/3, fill='red', font='Arial 24', text=instruction, justify='center')

        # Display level and consecutive correct info - aligned to top right
        level_info = f'Level: {current_level} | Consecutive: {consecutive_correct}/2'
        canvas.create_text(Width - 200, 80, fill='purple', 
                          font='Arial 18 bold', text=level_info, tags='level_info')

        score_text = canvas.create_text(Width - 200, 50, fill='darkgreen', 
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
                                   font='Times 160', text=seq_digits[a], justify='center')
            canvas.after(1000, canvas.update())
            canvas.delete(z)
            # Small pause between digits
            canvas.after(200, canvas.update())

        label = canvas.create_text(Width/2, Height/3.5, fill='darkblue', 
                                   font='Arial 26', text='Repeat the sequence here', justify='center')
        
        # Show instruction again
        instruction_reminder = "Enter REVERSED sequence" if reverse_required else "Enter sequence normally"
        canvas.create_text(Width/2, Height/3, fill='red', 
                          font='Arial 20', text=instruction_reminder, justify='center')

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
            total_time = int(time.time() - total_test_start_time)
            canvas.delete('all')
            
            # Get player name for leaderboard
            player_name = simpledialog.askstring("Game Over", "Enter your name for the leaderboard:", initialvalue="Player")
            if not player_name:
                player_name = "Anonymous"
            
            # Add to leaderboard
            leaderboard = add_to_leaderboard(player_name, SCORE, current_level, mode, total_time)
            
            # Check if it's a high score
            player_rank = None
            for i, entry in enumerate(leaderboard):
                if entry['name'] == player_name and entry['score'] == SCORE and entry['level'] == current_level:
                    player_rank = i + 1
                    break
            
            # Display results
            canvas.create_text(Width/2, Height/4, fill='darkblue', 
                               font='Arial 36', text='Game Over. Here are your results:', justify='center')
            canvas.create_text(Width/2, Height/2.8, fill='darkblue', 
                               font='Arial 28', text=f'Total Score: {SCORE}', justify='center')
            canvas.create_text(Width/2, Height/2.5, fill='purple', 
                               font='Arial 24', text=f'Highest Level Reached: {current_level}', justify='center')
            canvas.create_text(Width/2, Height/2.2, fill='darkgreen', 
                               font='Arial 20', text=f'Entries: {len(userNumbers)} | Total Time: {total_time} seconds', justify='center')
            
            # Show rank if high score
            if player_rank and player_rank <= 10:
                rank_text = f"🎉 NEW HIGH SCORE! Rank #{player_rank} 🎉"
                canvas.create_text(Width/2, Height/2, fill='gold', 
                                   font='Arial 22 bold', text=rank_text, justify='center')
            
            canvas.create_text(Width/2, Height/1.8, fill='blue', 
                               font='Arial 20 italic', text=random.choice(motivational_lines), justify='center')
            
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
                
            canvas.create_text(Width/2, Height/1.5, fill='orange', 
                               font='Arial 24', text=f'Attention Level: {attention_level}', justify='center')
            
            # Buttons
            menu_btn = tk.Button(wdw, height=2, width=15, text='Main Menu', 
                                 font='Arial 18', fg='white', command=show_main_menu, bd=0)
            menu_btn.configure(bg='#4682B4', activebackground='#36648B')
            canvas.create_window(Width/2 - 120, Height - 100, window=menu_btn)
            
            leaderboard_btn = tk.Button(wdw, height=2, width=15, text='View Leaderboard', 
                                        font='Arial 18', fg='white', command=show_leaderboard, bd=0)
            leaderboard_btn.configure(bg='#FF8C00', activebackground='#FF4500')
            canvas.create_window(Width/2 + 120, Height - 100, window=leaderboard_btn)

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
                                   font='Arial 26', text='Correct! Continue...', justify='center')
                
                # Show progress towards next level
                if consecutive_correct < 2:
                    progress_text = f"Consecutive correct: {consecutive_correct}/2 - Keep going!"
                    canvas.create_text(Width/2, Height/2, fill='orange', 
                                      font='Arial 18', text=progress_text, justify='center')
                else:
                    level_up_text = f"Level up! Moving to Level {current_level + 1}"
                    canvas.create_text(Width/2, Height/2, fill='purple', 
                                      font='Arial 20 bold', text=level_up_text, justify='center')
                
                motivation = random.choice(motivational_lines)
                canvas.create_text(Width/2, Height/1.6, fill='green', 
                                   font='Arial 20 italic', text=motivation, justify='center')
                canvas.after(2000, delete)  # Slightly longer delay to show level progress
            else:
                SCORE -= 2
                consecutive_correct = 0  # Reset consecutive counter on wrong answer
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                   font='Arial 26', text='Incorrect! Try again!', justify='center')
                canvas.create_text(Width/2, Height/2, fill='red', 
                                  font='Arial 18', text='Consecutive progress reset', justify='center')
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
                              font='Arial 20', text='Repeating sequence (consecutive progress reset)', justify='center')
            canvas.after(1000, canvas.update())
            
            for a in range(len(sequence_store['current'])):
                z = canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                       font='Times 160', text=sequence_store['current'][a], justify='center')
                canvas.after(1000, canvas.update())
                canvas.delete(z)
                canvas.after(200, canvas.update())
            runTest()

        def recognize_speech():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                canvas.create_text(Width/2, Height/1.8, fill='green', 
                                   font='Arial 20', text='Listening...', tag='listen_msg', justify='center')
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
                                       font='Arial 20', text='Could not understand. Try again.', tag='listen_msg', justify='center')
                except sr.RequestError:
                    canvas.delete('listen_msg')
                    canvas.create_text(Width/2, Height/1.8, fill='red', 
                                       font='Arial 20', text='Speech service failed.', tag='listen_msg', justify='center')

        def toggle_pause():
            global paused
            paused = not paused
            if paused:
                canvas.create_text(Width/2, Height/1.1, fill='red', font='Arial 20 bold', text='Paused', tag='pause_msg', justify='center')
            else:
                canvas.delete('pause_msg')
                runTest()

        entry.bind('<Return>', get_text)

        # Button positioning - better spacing and screen utilization
        button_continue = tk.Button(wdw, height=2, width=12, text='Continue', 
                                    font='Arial 20', fg='black', command=get_text, bd=0)
        button_continue.configure(bg='#4682B4', activebackground='#36648B', activeforeground='white')
        canvas.create_window(Width/2, Height - 300, window=button_continue)

        speak_btn = tk.Button(wdw, height=2, width=12, text='Speak',
                              font='Arial 20', fg='black', command=recognize_speech, bd=0)
        speak_btn.configure(bg='#20B2AA', activebackground='#2E8B57', activeforeground='white')
        canvas.create_window(Width/2, Height - 240, window=speak_btn)

        repeat_btn = tk.Button(wdw, height=2, width=28, text='Repeat Sequence (-2 & Reset)',
                               font='Arial 16', fg='black', command=repeat_sequence, bd=0)
        repeat_btn.configure(bg='#FF8C00', activebackground='#FF4500', activeforeground='white')
        canvas.create_window(Width/2, Height - 180, window=repeat_btn)

        # Bottom buttons - properly spaced at bottom
        pause_btn = tk.Button(wdw, height=2, width=12, text='Pause',
                              font='Arial 16', fg='black', command=toggle_pause, bd=0)
        pause_btn.configure(bg='#B0C4DE', activebackground='#708090', activeforeground='white')
        canvas.create_window(Width/2 - 120, Height - 80, window=pause_btn)

        stop_btn = tk.Button(wdw, height=2, width=12, text='Stop Game',
                             font='Arial 16', fg='black', command=stop_game, bd=0)
        stop_btn.configure(bg='#DC143C', activebackground='#8B0000', activeforeground='white')
        canvas.create_window(Width/2 + 120, Height - 80, window=stop_btn)

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

# Initialize window
wdw = tk.Tk()
wdw.title('Enhanced Digit Span Test with Leaderboard')
Width = wdw.winfo_screenwidth()
Height = wdw.winfo_screenheight()
wdw.geometry("%dx%d" % (Width, Height))
canvas = tk.Canvas(wdw, bg='#FDF5E6')
canvas.pack(fill='both', expand=True)
wdw.state('zoomed')

# Initialize global variables
i = 0
DIGITS = 3
FAILURES = 0
SCORE = 0
paused = False
consecutive_correct = 0
current_level = 1
userNumbers, generatedNumbers = [], []
start_time = 0
total_test_start_time = 0

# Show main menu
show_main_menu()

# Bind Enter key to start
wdw.bind('<Return>', lambda event: startTest('number'))

wdw.mainloop()

print('Generated: ', generatedNumbers)
print('Repeated:  ', userNumbers)