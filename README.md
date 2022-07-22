## Introduction:
* Minesweeper is a popular single-player logic/puzzle game. 

* In Minesweeper, you are given a grid of rectangular cells. Cells may or may not contain a mine. 

* The cells all start in a "hidden" state. When "revealed," a cell will tell the player how many of its neighbors are mines.

* The objective is to reveal all "safe" cells while not revealing any mines.

* Not all boards are solvable: it may be impossible to determine whether or not a cell is a mine, so guessing can be necessary.

## About:
* This project is a Minesweeper game implemented in Pygame which showcases a Minesweeper-solving algorithm I programmed.

* In addition to the features included in many standard implementations of Minesweeper, Minesweeper-SAT lets the player use a Minesweeper solver to assist them
in solving difficult boards.

* Furthermore, Minesweeper-SAT gives players the option to only play on boards which are guaranteed to be solvable without guessing. 
As an avid Minesweeper player myself, I found it frustrating that many boards could not be solved without guesswork!

<br/>

![ui_screenshot](https://user-images.githubusercontent.com/60950907/178075433-65b3c351-c9ff-4b3f-a24c-079886db743a.png)

## Methodology:
* Minesweeper solving algorithm:

  * Given the values of all revealed cells, the algorithm will decide whether each hidden cell is safe, mined, or impossible to determine without more information.
  
  * The algorithm views Minesweeper as a Boolean-satisfiability (SAT) problem. The variables are the cell states, with __True__ indicating the cell has a mine. 
  The constraints are obtained from the values on the revealed cells. The algorithm uses these to construct a prepositional formula in conjunctive normal form.  
  
  * Using pysat, a library for solving SAT problems, the algorithm exhausts all solutions to the prepositional formula.
  
  * Going through the solutions, the algorithm extracts all variables which have only one value: these are guaranteed to be mines or safe cells.
  
  * This process can be repeated using the new information obtained from revealing the safe cells.
  
 <br/>
 
![solver_screenshot](https://user-images.githubusercontent.com/60950907/178075432-f6777836-3d44-4528-b527-46bb499977a8.png)

 <br/>
 
* Solvable board generation:

  * To generate board that are solvable without guessing, I repeatedly generate normal Minesweeper boards (by randomly distrubuting, say, 99 mines among a 16x30 grid)
  until I get one that is solvable by the Minesweeper solving algorithm.
  
  * The downside is that my Minesweeper algorithm isn't very fast, and a surprising proportion of boards require guessing. To generate a no-guessing board
  could require many attempts, taking anywhere between <1s to sometimes >20s.
  
## Controls:
Keys | Actions
---|---
  _Left Click_ | Reveal cell or interact with interface
  _Right Click_ | Flag cell

## Requirements:
This project uses Python 3 and several external libraries (pysat, networkx, bidict, pygame). You can install the requirements by using:

    pip install -r requirements.txt

## Execution:
Either clone this repository using:

    git clone https://github.com/jwang541/Minesweeper-SAT.git
    
 __OR__ download the repository as a zip and extracting its contents. 
 
<br/>

Then, you can run minesweeper_game.py from the terminal:
    
    python game.py
    
 __OR__
 
    python3 game.py
    
 __OR__ find and open the game.py file.
