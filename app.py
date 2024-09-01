from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the board with empty cells
board = [""] * 9

# Function to reset the board
def reset_board():
    global board
    board = [""] * 9

# Function to check for a win
def check_winner(board, player):
    win_patterns = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for pattern in win_patterns:
        if all(board[i] == player for i in pattern):
            return True
    return False

# Function to find the best move for AI using minimax
def minimax(new_board, player):
    # Possible moves
    avail_spots = [i for i, spot in enumerate(new_board) if spot == ""]

    if check_winner(new_board, "X"):
        return {"score": -10}
    elif check_winner(new_board, "O"):
        return {"score": 10}
    elif len(avail_spots) == 0:
        return {"score": 0}

    moves = []
    for spot in avail_spots:
        move = {}
        move["index"] = spot
        new_board[spot] = player

        if player == "O":
            result = minimax(new_board, "X")
            move["score"] = result["score"]
        else:
            result = minimax(new_board, "O")
            move["score"] = result["score"]

        new_board[spot] = ""
        moves.append(move)

    best_move = None
    if player == "O":
        best_score = -10000
        for move in moves:
            if move["score"] > best_score:
                best_score = move["score"]
                best_move = move
    else:
        best_score = 10000
        for move in moves:
            if move["score"] < best_score:
                best_score = move["score"]
                best_move = move

    return best_move

@app.route('/')
def index():
    reset_board()  # Reset board when loading the page
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board
    data = request.get_json()
    index = data['index']
    board[index] = "X"

    # Check if player wins
    if check_winner(board, "X"):
        return jsonify({"board": board, "winner": "X"})

    # AI move using minimax
    ai_move = minimax(board, "O")
    if "index" not in ai_move:
        return jsonify({"board": board, "draw": True})  # Handle the edge case of draw

    board[ai_move["index"]] = "O"

    # Check if AI wins
    if check_winner(board, "O"):
        return jsonify({"board": board, "winner": "O"})

    # Check for a draw (no empty spots and no winner)
    if all(cell != "" for cell in board):
        return jsonify({"board": board, "draw": True})

    return jsonify({"board": board})

@app.route('/reset', methods=['POST'])
def reset():
    reset_board()
    return jsonify({"message": "Game reset"})

if __name__ == '__main__':
    app.run(debug=True)
