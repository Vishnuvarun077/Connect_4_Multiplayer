# Connect 4 Multiplayer Game

The Connect 4 Multiplayer Game is a classic two-player strategy game implemented using Pygame and sockets for network communication. The objective of the game is to be the first player to connect four of their colored discs (either red or yellow) in a row, column, or diagonal.

## Features

- **Multiplayer Functionality**: The game supports two-player gameplay, where one player acts as the server and the other as the client.
- **Interactive Game Board**: The game board is represented as a 2D grid, and players can drop their discs by clicking on the desired column.
- **Animation and Visual Effects**: Particle and bubble animations provide visual feedback when a disc is dropped, enhancing the overall user experience.
- **Game Logic and Winning Conditions**: Functions check for winning conditions (four connected discs) and draw conditions (the board is full).
- **Scoreboard and Active Player Indication**: The game displays the current score for each player and indicates the active player.
- **Restart and End Game Functionality**: Players can restart the game or end it entirely, providing flexibility and control.
- **Error Handling and Cleanup**: The code includes error handling mechanisms for network communication and Pygame-related operations. Resources are properly cleaned up when the game is exited.

## Demo and Instructions

1. **Clone the repository**:

`git clone https://github.com/Vishnuvarun077/Connect-4-Multiplayer-Game.git`

2. **Navigate to the project directory**:

`cd Connect-4-Multiplayer-Game`

3. **Run the game**:
`python connect4_multiplayer.py`

4. Make sure the other player also runs the same commands menttioned above. If the both players are playing in the same pc make sure to run these files in two seperate terminals.
5. When prompted, choose whether you want to be the server or the client:
- If you choose to be the server, the game will wait for a client to connect.
- If you choose to be the client, the game will prompt you to enter the server's IP address.

6. Once the connection is established, the game will start, and you can begin playing:
- Click on a column to drop your piece.
- The first player to connect four pieces in a row, column, or diagonal wins the game.

7. You can restart the game or end it using the respective buttons.


