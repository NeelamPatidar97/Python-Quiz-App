from tkinter import *
from tkinter import ttk
from tkinter import messagebox  # Import messagebox for displaying warnings
from PIL import Image, ImageTk

#define question dictionary
question = {
	"1. What year was Python created?": ['1989', '1991', '2000', '2016'],
    "2. Which of these is not a mutable built-in type Python?": ['Sets', 'Lists', 'Tuples', 'Dictionary'],
    "3. What is a correct syntax to output \"Hello World\" in Python?": ['print("Hello World")', 'echo("Hello World")', 'p("Hello World")', 'echo "Hello World"'],
    "4. Why is this code below often added to a Python program file?\nif __name__ == '__main__':\n    main()": ['It allows us to skip calling the main() function by defining an environment variable.', 'It executes the main() function only if this file is executed as the main program.', 'It assures that the program will run correctly when executed from either an IDE or command line.', 'It confirms that it is an actual Python program before starting the interpreter.'],
    "5. What is the proper syntax for accessing the fourth element of the following sequence?\nvalues = [1, 3, 5, 7, 9, 11, 13]": ['values{3}', 'values[4]', 'values(4)', 'values[3]'],
    "6. Class Fruit is derived from the class Food. Which is the correct way for Fruit to call a function of its parent class?": ['super().SetPrice(50)', 'super.SetPrice(50)', 'parent().SetPrice(50)', 'super().SetPrice(self,50)'],
    "7. What is the output of the following code?\nvar = \"James Bond\"\nprint(var[2::-1])": ['Jam', 'dno', 'maJ', 'dnoB semaJ'],
    "8. What is the output of the following code?\nsampleList = ['Jon', 'Kelly', 'Jessa']\nsampleList.append(2, 'Scott')\nprint(sampleList)": ['The program executed with errors', '[‘Jon’, ‘Kelly’, ‘Scott’, ‘Jessa’]', '[‘Jon’, ‘Kelly’, ‘Jessa’, ‘Scott’]', '[‘Jon’, ‘Scott’, ‘Kelly’, ‘Jessa’]'],
    "9. What is the output of the following code?\nlistOne = [20, 40, 60, 80]\nlistTwo = [20, 40, 60, 80]\nprint(listOne == listTwo)\nprint(listOne is listTwo)": ['True\nTrue', 'True\nFalse', 'False\nTrue'],
	"10. How do you insert COMMENTS in Python code?":['#This is a comment','//This is a comment','/*This is a comment*/']
}

#define answer list
ans = ['1', '2', '0', '1', '3', '0', '2', '0', '1', '0']


current_question = 0
quiz_time_limit = 600
timer_id = None

def apply_style():
    # Cal State LA Colors
    gold_color = "#ffc627"  # Gold-like color used for text
    black_color = "#000000"  # Black color used for the background
    white_color = "#ffffff" 


    style = ttk.Style()
    style.theme_use('clam')  # Use a theme that allows for more customization

    style.configure('TFrame', background=black_color)
    style.configure('TLabel', background=black_color, foreground=gold_color, font=('Product Sans', 12))
    style.configure('Start.TButton', font=('Product Sans', 10, "bold"), background=gold_color, foreground=black_color)
    # Configure the style for TButton in case Start.TButton doesn't get applied
    style.configure('TButton', font=('Product Sans', 10, "bold"), background=gold_color, foreground=black_color)
    style.configure('TRadiobutton', background=black_color, foreground=white_color, font=('Product Sans', 10))

    
    # Configure the color of the button when it is active (being clicked)
    style.map('Start.TButton', background=[('active', gold_color)], foreground=[('active', black_color)])
    
    root.configure(bg=black_color)

def start_quiz():
    intro_frame.pack_forget()
    img_label.pack_forget()
    start_button.pack_forget()
    next_button.pack(side=BOTTOM, pady=20)
    f1.pack(fill=BOTH, expand=True, padx=20, pady=20)
    next_question()
    update_timer()  # This starts the timer

def next_question():
    global current_question
    if current_question < len(question):
        check_ans()
        user_ans.set(None)  # Reset selected radio button
        clear_frame()
        question_text = list(question.keys())[current_question]
        ttk.Label(f1, text=f"Question {question_text}", font=("Product Sans", 12, "bold"), wraplength=800).pack(anchor="w", padx=20, pady=10)
        for value, option in enumerate(question[question_text]):
            ttk.Radiobutton(f1, text=option, variable=user_ans, value=option, style="TRadiobutton").pack(anchor="w", padx=40)
        current_question += 1
    else:
        finalize_quiz()

def check_ans():
    global current_question  # Ensure you can access and modify the current question index
    temp_ans = user_ans.get()
    if temp_ans:
        # Determine if the answer is correct
        correct_answer = question[list(question.keys())[current_question - 1]][int(ans[current_question - 1])]
        if temp_ans == correct_answer:
            feedback = "Correct Answer!"
            user_score.set(user_score.get() + 1)  # Increment the score for a correct answer
        else:
            feedback = "Incorrect Answer!"
        
        # Display feedback
        feedback_label = ttk.Label(f1, text=feedback, font=("Product Sans", 10, "bold"), foreground="green" if feedback == "Correct Answer!" else "red")
        feedback_label.pack(anchor="s", pady=5)
        root.update_idletasks()  # Update the GUI to ensure the feedback is displayed before moving on
        root.after(1000)  # Wait for 1 second. Adjust the timing as necessary.
        feedback_label.destroy()  # Remove the feedback message before the next question

        

def finalize_quiz():
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)  # Cancel the scheduled timer update
        timer_id = None  # Reset timer_id
        
    next_button.pack_forget()
    # Removed the call to check_ans() here as it's not needed at the end of the quiz
    clear_frame()
    total_questions = len(question)
    correct_answers = user_score.get()
    score_percent = (correct_answers / total_questions) * 100
    ttk.Label(f1, text="Thank you for your participation.", font=("Product sans", 14)).pack()
    output = f"You answered {correct_answers} out of {total_questions} questions correctly - Your score is {score_percent:.1f}%."
    ttk.Label(f1, text=output, font=("Product Sans", 14)).pack(pady=20)
    if score_percent == 100:
        ttk.Label(f1, text="You nailed it, well done!", font=("Product Sans", 14)).pack()
        finish_button = ttk.Button(f1, text="Terminate Quiz", command=root.destroy)  # Button to exit the quiz
        finish_button.pack(pady=20)
    else:
        ttk.Label(f1, text="You can re-take the quiz until you get a 100%!", font=("Product Sans", 12)).pack()
        # Add Retake Quiz Button
        ttk.Button(f1, text="Retake Quiz", command=retake_quiz).pack(pady=20)

def retake_quiz():
    global current_question, quiz_time_limit
    current_question = 0
    quiz_time_limit = 600  # Reset the timer to 10 minutes
    user_score.set(0)  # Reset the user's score
    clear_frame()
    f1.pack_forget()
    intro_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    img_label.pack(pady=10)
    start_button.pack(side=BOTTOM, pady=20)
    time_left_var.set("Timer : 10:00")  # Reset the timer display
   
    

def clear_frame():
    for widget in f1.winfo_children():
        widget.destroy()

def update_timer():
    global quiz_time_limit, timer_id  # Add timer_id to the global declaration
    current_time = quiz_time_limit - 1
    minutes, seconds = divmod(current_time, 60)
    time_left_var.set("{:02d}:{:02d}".format(minutes, seconds))
    if current_time > 0:
        quiz_time_limit = current_time
        timer_id = root.after(1000, update_timer)  # Store the ID of the scheduled call
    else:
        finalize_quiz()


if __name__ == "__main__":
    root = Tk()
    root.title("5040 Project - Python Knowledge Quiz")
    root.geometry("900x600")
    root.resizable(True, True)

    apply_style()

     # Load and Resize the Logo Image
    background_color = "black"
    logo_path = "C:\\Users\\npatida\\Desktop\\Quiz\\Logo.png"  # Make sure to replace this with the actual path to your logo
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((100, 100))  # Resize the logo appropriately
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Ensure that the logo's label background matches the root window's background
    logo_label = Label(root, image=logo_photo, bg="Black")  # Use the black background color
    logo_label.image = logo_photo  # Keep a reference
    logo_label.pack(anchor='nw', padx=5, pady=5)  # Pack it first to ensure it's at the top


    # Timer settings
    quiz_time_limit = 600  # 600 seconds for the entire quiz
    time_left_var = StringVar()
    time_left_var.set("Timer : 10:00")  # Starting time displayed as mm:ss

    # Timer display label
    timer_label = ttk.Label(root, textvariable=time_left_var, font=("Product Sans", 14, "bold"), background='Black', foreground='gold')
    timer_label.pack(pady=10)  # Adjust placement as needed

    # Style Configuration
    s = ttk.Style()
    s.configure('TRadiobutton', font=('Product Sans', 10))

    # Variables
    user_ans = StringVar(value=None)
    user_score = IntVar(value=0)
    current_question = 0

    # Title Label
    ttk.Label(root, text="Python Knowledge Quiz", font=("Product Sans", 18, "bold"), foreground="white").pack(pady=20)


    # The PhotoImage class only supports PNG and GIF images.
    quiz_image = PhotoImage(file="C:\\Users\\npatida\\Desktop\\Quiz\\QuizImg.png")
    quiz_image = quiz_image.subsample(2, 2)  # Resample to 1/2 of the original size
    img_label = Label(root, image=quiz_image)
    img_label.pack(pady=10)

    # Introductory Text Frame
    intro_frame = ttk.Frame(root)
    intro_text = "Step right up to the Python challenge! Ten quickfire questions to prove you're a code wizard. Ready to roll?"
    ttk.Label(intro_frame, text=intro_text, font=("Product Sans", 12),foreground="white", wraplength=800).pack(pady=20)
    intro_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Start Quiz Button
    start_button = ttk.Button(root, text="Start Quiz", command=start_quiz, style='Start.TButton')
    start_button.pack(side=BOTTOM, pady=20)
    


    # Question Frame (hidden until the quiz starts)
    f1 = ttk.Frame(root, style='TFrame')


    # Next Question Button (hidden until the quiz starts)
    next_button = ttk.Button(root, text="Next Question", command=next_question)

    root.mainloop()