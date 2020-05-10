## Goblin-Slayer---Pygame ##

## A goblin mindlessly walks back and forth, you must slay him. ##


This was the first game I created utilizing the Pygame module.

Using the fundamentals of Object-Oriented Programming, I created a basic arcade style game that executes through a main loop. All animations and soundbites of this game are displayed through a series of .png's, .jpgs, .wav's, and .mp3's. In order to allow the main scripts to execute properly, these animation files must be stored in the same directory as the firstGame.py script. 

This was done to in efforts of preserving the simplicity of the firstGame.py script, as the Pygame module loads the collection of animations and soundbites by calling the filename without stating its directory.

The three main objects in this game are the player, enemy, and the projectile. The player and enemy share similar class attributes and methods, but differ in the way that they move, hit, and update. This grants the player the ability to move freely as they wish, while the enemy is set moving monotonously back and forth across the screen. Health is updated for the goblin simultaneously as he is hit with a projectile. Instead of health for the player, collision dictates the score of the game.  

This was done by giving both the player and the goblin a hitbox, if the X and Y positions of both hitboxes overlap, the player loses 5 points. Once the player's points become negative, the script quits running. If the player defeats the goblin the script also quits.  
