from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# Global variables for game state
number_to_guess = random.randint(1, 100)
attempts = 0
message = "Guess a number between 1 and 100!"

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Number Guessing Game</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
                h1 { color: #333; }
                p { font-size: 18px; }
                a { font-size: 20px; text-decoration: none; color: white; background: #007BFF; padding: 10px 20px; border-radius: 5px; }
                a:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <h1>Welcome to the Number Guessing Game!</h1>
            <p>Think you can guess the correct number?</p>
            <a href="/number_game">Start the Game</a>
        </body>
        </html>
    ''')

@app.route('/number_game', methods=['GET', 'POST'])
def number_game():
    global number_to_guess, attempts, message

    if request.method == 'POST':
        user_input = request.form.get('guess', '').strip()

        if user_input.isdigit():
            guess = int(user_input)
            attempts += 1

            if guess < number_to_guess:
                message = "Too low! Try again."
            elif guess > number_to_guess:
                message = "Too high! Try again."
            else:
                message = f"🎉 Correct! You guessed the number in {attempts} attempts."
                # Reset the game after a correct guess
                number_to_guess = random.randint(1, 100)  # Reset the number
                attempts = 0  # Reset attempts
        else:
            message = "⚠️ Please enter a valid number!"

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Number Guessing Game</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
                h1 { color: #333; }
                form { margin-top: 20px; }
                input[type="number"] { padding: 10px; font-size: 16px; margin-right: 10px; }
                input[type="submit"], .reset-btn {
                    padding: 10px 15px;
                    font-size: 16px;
                    cursor: pointer;
                    background: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                input[type="submit"]:hover, .reset-btn:hover {
                    background: #218838;
                }
                .reset-btn {
                    margin-top: 20px;
                    display: inline-block;
                    text-decoration: none;
                }
                .message { margin-top: 20px; font-size: 18px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Number Guessing Game</h1>
            <p>Guess the number between 1 and 100!</p>
            <form method="POST">
                <input type="number" name="guess" placeholder="Enter your guess" required>
                <input type="submit" value="Submit">
            </form>
            <div class="message">{{ message }}</div>
            <form method="GET" action="/number_game">
                <button class="reset-btn">Reset Game</button>
            </form>
        </body>
        </html>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=True)
