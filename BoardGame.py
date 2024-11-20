#Example Flask App for a hexaganal tile game
#Logic is in this python file

from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Game state: A simple 8x8 board
game_state = {
    "board": [
        [None, "red", None, "red", None, "red", None, "red"],
        ["red", None, "red", None, "red", None, "red", None],
        [None, "red", None, "red", None, "red", None, "red"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["white", None, "white", None, "white", None, "white", None],
        [None, "white", None, "white", None, "white", None, "white"],
        ["white", None, "white", None, "white", None, "white", None]
    ],
    "turn": "white",  # "white" starts the game
    "white_pieces": 12,
    "red_pieces": 12,
}

@app.route('/')
def index():
    return render_template('index.html', board=game_state["board"])

@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    return jsonify(game_state)

@app.route('/move_piece', methods=['POST'])
def move_piece():
    data = request.get_json()
    start_row, start_col = data['start']
    end_row, end_col = data['end']

    # Validate move, update board, and change turn
    piece = game_state["board"][start_row][start_col]
    
    if piece != game_state["turn"]:
        return jsonify({"error": "Not your turn!"}), 400

    if not valid_move(start_row, start_col, end_row, end_col, piece):
        return jsonify({"error": "Invalid move!"}), 400

    # Update board, flip piece if needed, jump opponent's piece if applicable
    game_state["board"][end_row][end_col] = piece
    game_state["board"][start_row][start_col] = None

    if (end_row == 0 and piece == "white") or (end_row == 7 and piece == "red"):
        # Flip the piece to crown if it reaches the opponent's side
        game_state["board"][end_row][end_col] = piece + "_crown"

    # Switch turns
    game_state["turn"] = "red" if game_state["turn"] == "white" else "white"

    return jsonify(game_state)

def valid_move(start_row, start_col, end_row, end_col, piece):
    # Logic to validate moves and jumps goes here
    return True

if __name__ == '__main__':
    app.run(debug=True)
