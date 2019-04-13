# Introduction
1.9 percent of Americans suffer from paralysis, meaning roughly 5.4 million people who can’t walk, write, or ever have any form of interactive entertainment. In today’s world, almost all American children play videogames, and our project brings these same experiences to those who are paralyzed. We have created a game that relies solely on head motion. The game is a car racing/dodging game, which is operated by tilting the user’s head to operate the car.  To do this, we used a combination of the OpenCV library, the Google Cloud Vision API, Pygame, and the python Multithreading Pool. The game0i	 With more development, we can add more features including powerups and perhaps a nitro boost. We can also further experiment with different forms of head rotation.

## Inspiration
One of our team members has a family member who suffers from paralysis on the left side of the body, and he really made the rest of the team understand the struggles that these people have. 
To make life more entertaining for people who suffer from this disease, we made a game that solely relies on head movement.
## What it does
The game is a car racing and obstacle dodging game. The player rotates his head to make the car move in real time on the screen. 
## How we built it
We used Google's Vision API to process the angle of the head, and pygame to implement the game in Python. To continuously capture the player's head with the webcam we used OpenCV for Python. 
## Challenges we ran into 
Google's Vision API was computationally intensive, so it started holding up our main thread. It took us a long time to figure out how to move the computation to another thread in Python.

## Accomplishments that we're proud of
We are proud of figuring out to how to use Google's Vision API and being able to make a game in Python.

## What we learned 
We learned that you sometimes have to keep on working hard to fix technical difficulties. 

## What's next for Car Game with Head Rotation
There are many improvements that we can make to Car Game with rotation. First of all, the game itself can be optimized further. The game sometimes locks up. Secondly, we can add an option for those whose paralysis disables them from moving their head in a specific way, and adding the code that can accomodate them. We can also add a multiplayer mode which can have people compete against their family members and or their friends. Lastly, the graphics can be improved. 

# Contributors
Akshar Yecherla,
Kenan Hasanaliyev,
Aditya Gupta,
Pranav Konda
