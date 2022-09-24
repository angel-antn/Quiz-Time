import time
import tkinter as tk
from quiz_brain import QuizBrain
import playsound
from data import have_internet

BACKGROUND = '#91a9f5'
FOREGROUND = '#8338ec'

FONT_TITLE = ('Arial Black', 24, 'bold')
FONT = ('Gill Sans MT', 18, 'bold')
FONT_RESULT = ('Arial Black', 32, 'bold')


class Gui:

    def __init__(self):

        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.title('Quiz Time!')
        self.window.config(padx=90, pady=40, bg=BACKGROUND)

        self.logo = tk.PhotoImage(file='img/logo.png')
        self.title = tk.PhotoImage(file='img/title.png')
        self.board = tk.PhotoImage(file='img/board.png')
        self.right_board = tk.PhotoImage(file='img/right_board.png')
        self.wrong_board = tk.PhotoImage(file='img/wrong_board.png')
        self.button = tk.PhotoImage(file='img/button.png')
        self.true_button = tk.PhotoImage(file='img/true_button.png')
        self.false_button = tk.PhotoImage(file='img/false_button.png')
        self.icon = tk.PhotoImage(file='img/icon.png')

        self.window.iconphoto(False, self.icon)

        if not have_internet():
            self.no_internet()
        else:
            self.brain = QuizBrain()
            playsound.playsound('sounds/Intro.mp3', False)
            self.intro()

    def intro(self):
        def to_game():
            canvas.destroy()
            button.destroy()
            self.game()

        canvas = tk.Canvas(width=424, height=340, highlightthickness=0, bg=BACKGROUND)
        canvas.create_image(212, 170, image=self.logo)
        canvas.grid(row=0)

        button = tk.Button(text='Play Now!', command=to_game, image=self.button, compound='center', font=FONT_TITLE,
                           fg='white', bg=BACKGROUND, relief=tk.FLAT, borderwidth=0, activeforeground='white',
                           activebackground=BACKGROUND, cursor='hand2')
        button.grid(row=1, pady=20)

    def game(self):

        def true():
            is_correct = self.brain.next_question('True')

            if is_correct:
                canvas_board.itemconfig(board, image=self.right_board)
                playsound.playsound('sounds/Heeey.mp3', False)
            else:
                canvas_board.itemconfig(board, image=self.wrong_board)
                playsound.playsound('sounds/Awww.mp3', False)

            keep_on(self.brain.still_have_questions())

        def false():
            is_correct = self.brain.next_question('False')

            if is_correct:
                canvas_board.itemconfig(board, image=self.right_board)
                playsound.playsound('sounds/Heeey.mp3', False)
            else:
                canvas_board.itemconfig(board, image=self.wrong_board)
                playsound.playsound('sounds/Awww.mp3', False)

            keep_on(self.brain.still_have_questions())

        def clean_board():
            canvas_board.itemconfig(board, image=self.board)
            true_button.config(state=tk.ACTIVE)
            false_button.config(state=tk.ACTIVE)

        def keep_on(are_questions_left):
            true_button.config(state=tk.DISABLED)
            false_button.config(state=tk.DISABLED)

            if are_questions_left:
                self.window.after(1000, clean_board)
                canvas_board.itemconfig(question, text=self.brain.get_question())
                score.config(text=f'Score {self.brain.score}/10')
            else:
                score.destroy()
                self.window.after(1000, result)

        def result():
            time.sleep(1)
            canvas_board.itemconfig(board, image=self.board)
            canvas_board.itemconfig(question, text=f'Result: {self.brain.score}/10', font=FONT_RESULT)
            playsound.playsound('sounds/Silbato.mp3', False)
            self.window.after(3000, to_intro)

        def to_intro():
            canvas_title.destroy()
            canvas_board.destroy()
            true_button.destroy()
            false_button.destroy()
            if not have_internet():
                self.no_internet()
            else:
                self.brain.clean()
                self.intro()

        canvas_title = tk.Canvas(width=308, height=68, background=BACKGROUND, highlightthickness=0)
        canvas_title.create_image(154, 34, image=self.title)
        canvas_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        score = tk.Label(text=f'Score {self.brain.score}/10', foreground='white',
                         font=FONT, background=BACKGROUND)
        score.grid(row=0, column=1, sticky='NE')

        canvas_board = tk.Canvas(width=648, height=360, background=BACKGROUND, highlightthickness=0)
        board = canvas_board.create_image(324, 180, image=self.board)
        question = canvas_board.create_text(300, 200, text=self.brain.get_question(), font=FONT, width=350,
                                            fill=FOREGROUND, justify='center')
        canvas_board.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        true_button = tk.Button(text='True', command=true, image=self.true_button, compound='center',
                                font=FONT_TITLE, fg='white', bg=BACKGROUND, relief=tk.FLAT, borderwidth=0,
                                activeforeground='white', activebackground=BACKGROUND, cursor='hand2',
                                disabledforeground='white')
        true_button.grid(row=2, column=0)

        false_button = tk.Button(text='False', command=false, image=self.false_button, compound='center',
                                 font=FONT_TITLE, fg='white', bg=BACKGROUND, relief=tk.FLAT, borderwidth=0,
                                 activeforeground='white', activebackground=BACKGROUND, cursor='hand2',
                                 disabledforeground='white')
        false_button.grid(row=2, column=1)

    def no_internet(self):

        canvas = tk.Canvas(width=648, height=360, highlightthickness=0, bg=BACKGROUND)
        canvas.create_image(324, 180, image=self.board)
        canvas.create_text(300, 200, text='This game works with internet connection\n'
                                          'Try again later...', font=FONT, width=350,
                           fill=FOREGROUND, justify='center')
        canvas.grid(row=0, pady=50)
        playsound.playsound('sounds/Awww.mp3', False)
