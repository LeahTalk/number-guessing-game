from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
# our index route will handle rendering our form
@app.route('/')
def index():
    #initialize values if they don't exist yet in session
    if (not 'randomNum' in session) or (not 'userGuess' in session):
        session['randomNum'] = random.randint(1,100) 
        session['userGuess'] = -1
        session['numGuesses'] = 0
    #If user just refreshes the page without making a guess
    if(session['userGuess'] == -1):
        return render_template("index.html", box_class = 'no_guess', text_display = 'none', text_content = '', 
                                play_again_display = 'none', input_display = 'block', submit_display = 'inline-block',
                                guess_display = 'none', guess_text = "")
    if session['numGuesses'] >= 4:
        return render_template("index.html", box_class = 'wrong_guess', text_display = 'inline-block', text_content = 'You Lose!', 
                        play_again_display = 'inline-block', input_display = 'none', submit_display = 'none',
                        guess_display = 'inline-block', guess_text = "You ran out of guesses.")
    if int(session['userGuess']) > session['randomNum']:
        session['numGuesses'] += 1
        return render_template("index.html", box_class = 'wrong_guess', text_display = 'inline-block', text_content = 'Too High!', 
                                play_again_display = 'none', input_display = 'block', submit_display = 'inline-block', guess_display = 'inline-block', 
                                guess_text = "You have guessed " + str(session['numGuesses']) + " times. You have " + str(5 - session['numGuesses']) + " remaining.")
    if int(session['userGuess']) < session['randomNum']:
        session['numGuesses'] += 1
        return render_template("index.html", box_class = 'wrong_guess', text_display = 'inline-block', text_content = 'Too Low!', 
                            play_again_display = 'none', input_display = 'block', submit_display = 'inline-block', guess_display = 'inline-block', 
                            guess_text = "You have guessed " + str(session['numGuesses']) + " times. You have " + str(5 - session['numGuesses']) + " remaining.")
    if int(session['userGuess']) == session['randomNum']:
        session['numGuesses'] += 1
        return render_template("index.html", box_class = 'correct_guess', text_display = 'inline-block', text_content = str(session['userGuess']) + ' was the correct number!', 
                                play_again_display = 'inline-block', input_display = 'none', submit_display = 'none',
                                guess_display = 'inline-block', guess_text = "It took you " + str(session['numGuesses']) + " times to find the right number!")
    return render_template("index.html")

@app.route('/guess', methods = ['POST'])
def guess():
    session['userGuess'] = request.form['user_num']
    return redirect('/')

@app.route('/reset')
def resetKeys():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
