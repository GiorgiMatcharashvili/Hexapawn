# Hexapawn
My goal was to create Hexapawn and make AI as opponent of the user, which getting smarter after all lost game. I reached my goal, and after playing 20 minutes with my algorithm,
AI became invincible. Seriously, it becomes mathematically impossible to defeat.

# Description
Hexapawn, is a simple game, very simple. At first, you have 3x3 board, at bottom your three pawn is placed in row and your opponent's three pawn at the top.
 
![download](https://user-images.githubusercontent.com/76595828/123946903-c3f4bd80-d9b0-11eb-8ae1-a96cbeee1672.png)
  
Pawns can be moved forward, if place is not occupied and they can move diagonally, only if they take opponent's pawn.
 
There is three ways to win:
  1. reach end of the board,
  2. kill all the opponent's pawns,
  3. leave opponent without moves.

For more information: https://en.wikipedia.org/wiki/Hexapawn

# Getting started
If you want to run my game at your device for some reasons, you just need to clone my project and run Launch.py.
 
AI is already smart, so you have to delete moves.json to start from fresh.
 
# Using
When you click at blue square, it becomes more lighter, which means you select figure and you can move it, by clicking valid position.
When you click again at selected figure, it unselects and you can't move it, before you click again.
If you accidentally select wrong figure, you can click right one and it becomes selected automatically.
 
After You make move, AI choose it's moves and you can see how it's selects red figures and makes moves.
 
Text at the top of the board, shows which's turn to play(Blue or Red) and if someone wins game, it shows you the winner.

After end of the game, program shuts down.

# How AI works
If we consider what player starts first, one of the blue pawn is already moved forward. AI takes all occupied/unoccupied places, generates all possible moves, what
AI can do, and makes dicrionary out of this information, it gives ID to this dectionary, so it can find it easly in the future. AI puts all the information into the moves.json

After that it takes all the possible moves and plays one of them randomly. If AI loses after this move, that means it made bad move and it deletes from moves.json.
If the move was successful and AI wins, then it puts another move into the possible move, so successful move can be easly choosen in the future, when AI randomly choose from the list.

With this way, AI gets rid of bad moves and saves, even adds more good moves, so in the future, it makes only good moves.

At the start, AI is very simple to defeat, it does not know anything, but then you win couple of times, it getting smarter and never losing with the same way. For my calculation,you can win first 10 or 15 games, then AI gets smarter and you can't win that easy.
 
# Credits
@inc. all by myself
