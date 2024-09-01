let boxes = document.querySelectorAll(".box");
let resetBtn = document.querySelector("#reset-button");
let newGameBtn = document.querySelector("#new-button");
let msgContainer = document.querySelector(".msg_container");
let msg = document.querySelector("#msg");

let turnX = true; // Player's turn is X
let counter = 0;
let win = 0;

const updateBoard = (board) => {
    boxes.forEach((box, index) => {
        box.innerText = board[index];
    });
};

const resetGame = () => {
    turnX = true;
    counter = 0;
    win = 0;
    enableBoxes();
    msgContainer.classList.add("hide");
    updateBoard(["", "", "", "", "", "", "", "", ""]);

    // Send a request to reset the game on the server
    fetch("/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            }
        })
        .catch(error => console.error("Error resetting game:", error));
};

boxes.forEach((box, index) => {
    box.addEventListener("click", () => {
        if (!box.innerText) {
            box.innerText = "X";
            box.disabled = true;
            counter++;
            sendMoveToServer(index);
        }
    });
});

const sendMoveToServer = (index) => {
    fetch("/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                index: index
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.board) {
                updateBoard(data.board);
            }
            if (data.winner) {
                showWinner(data.winner);
                disableBoxes();
            } else if (data.draw) {
                showWinner("Draw");
                disableBoxes();
            }
        })
        .catch(error => console.error("Error:", error));
};

const disableBoxes = () => {
    boxes.forEach(box => box.disabled = true);
};

const enableBoxes = () => {
    boxes.forEach(box => {
        box.disabled = false;
        box.innerText = "";
    });
};

const showWinner = (winner) => {
    msg.innerText = winner === "Draw" ? "It's a Draw!" : `Congratulations, Winner is ${winner}`;
    msgContainer.classList.remove("hide");
};

newGameBtn.addEventListener("click", resetGame);
resetBtn.addEventListener("click", resetGame);