"Chess"

This program was written by Cullen Seaton as a hobby project to improve Python coding skills generally and in particular to gain experience with data structures, string handling, and artificial intelligence. It relies on some basic python libraries like "sys, "time", and "random" but all ai algorithms and data structures are completely homemade. This program is still under development.

Instructions for use:

To initiate, use the terminal to navigate to the correct directory and enter command “python main.py”.

"Chess" runs entirely in terminal using an intuitive script based interface. It will prompt player input by printing "=> "; responses should be in the form of a string of ASCII characters followed by "enter". This program is designed to read standard chess algebra as defined by the World Chess Federation. A description of this notation system can be found here:
https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

To surrender, type the string "QQ" after any prompt.

Example game:

***************************************************************

> python main.py

Welcome to Chess
This program is under development

Enter name for white player:
=> Cullen
Select player type:
	(1) Human
	(2) Computer
=> 1
Enter name for black player:
=> Deep Blue
Select player type:
	(1) Human
	(2) Computer
=> 2
1w
bR	bN	bB	bQ	bK	bB	bN	bR	


bP	bP	bP	bP	bP	bP	bP	bP	


0	0	0	0	0	0	0	0	


0	0	0	0	0	0	0	0	


0	0	0	0	0	0	0	0	


0	0	0	0	0	0	0	0	


wP	wP	wP	wP	wP	wP	wP	wP	


wR	wN	wB	wQ	wK	wB	wN	wR	


=> e4
e4
1b
bR	bN	bB	bQ	bK	bB	bN	bR	


bP	bP	bP	bP	bP	bP	bP	bP	


0	0	0	0	0	0	0	0	


0	0	0	0	0	0	0	0	


0	0	0	0	wP	0	0	0	


0	0	0	0	0	0	0	0	


wP	wP	wP	wP	0	wP	wP	wP	


wR	wN	wB	wQ	wK	wB	wN	wR	


....................
Nc6
2w
bR	0	bB	bQ	bK	bB	bN	bR	


bP	bP	bP	bP	bP	bP	bP	bP	


0	0	bN	0	0	0	0	0	


0	0	0	0	0	0	0	0	


0	0	0	0	wP	0	0	0	


0	0	0	0	0	0	0	0	


wP	wP	wP	wP	0	wP	wP	wP	


wR	wN	wB	wQ	wK	wB	wN	wR	


=> QQ
Cullen surrenders
Would you like to save the game log? (y/n)
=> y
Thanks for playing!
***************************************************************


Summary of Modules:

1. Main - Contains code to initiate the program and functions that handle high-level control flow.

2. Player Input - Contains functions that deal with gathering and verifying human input through the terminal.

3. Rules - Contains functions that test the legality of a specified move against the standard World Chess Federation rulebook.

4. Utilities - Contains functions to support string handling and to specify error messages

5. Classes - Contains all data structures and associated functions

6. Chess Bot - Contains all functions related to the operation of the artificial intelligence engine.
