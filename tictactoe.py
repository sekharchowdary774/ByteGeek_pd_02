from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global game state
board = [""] * 9
current_player = "X"

def check_winner():
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "Draw"
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    global current_player, board

    winner = check_winner()

    if request.method == "POST" and not winner:
        pos = int(request.form.get("position", -1))
        if 0 <= pos < 9 and board[pos] == "":
            board[pos] = current_player
            winner = check_winner()
            if not winner:
                current_player = "O" if current_player == "X" else "X"

    return render_template("index.html", board=board, winner=winner, current_player=current_player)

@app.route("/reset")
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return redirect(url_for("index"))

# Only for local testing — ignored in production by gunicorn
if __name__ == "__main__":
    app.run(debug=True)
