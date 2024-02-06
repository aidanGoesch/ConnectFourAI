# Connect Four AI
This program uses the minimax algorithm to make an AI opponenet in the game of Connect Four. To increase the efficiency of the algorithm, I use alpha-beta pruning to cut down on the number of nodes that the algorithm needs to search. In addition to this, I cache all of the function calls so that the algorithm can run in O(1) time when there is a recursive call that is identical to a previous function call.

## Instructions to Run
1. Clone the repository with `git clone git@github.com:aidanGoesch/MazeGenerator.git`

2. Run `cd ConnectFourAI` to switch into the repository directory

3. Install the external libraries with `pip install -r requirements.txt`

4. To run the script, use the command `python view.py` in the top level of the repository 
