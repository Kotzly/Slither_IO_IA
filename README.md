# Slither_IO_IA

To run this program, you need Python 3.6 with libraries:
- tkinter
- random
- PIL
- os
- time
- numpy
- scipy

If you don't have one, you can install it using:
- pip install library_name
or
- pip3 install library_name

SLITHER IO AG

Functions:
- Lenght: Choose the inital snake size, in segments.
- Width: The snake body segment diameter, in pixels.
- Segment Distance: The distance between segments's centers, in pixels.
- Brain config: The neural network topology:
    "5 5" will generate a neural network with 2 hidden layers, with 5 neurons in each.
    "10" will generate a neural network with 1 hidden layers, with 10 neurons.
    "15 10 5" will generate a neural network with 3 hidden layers, with 15 neurons in the first one, 10 on the second one and 5 on the last one.
- Snake vision range: A number N, in pixels. The snake sees a square NxN around it's own head.
- Snake max. turning: The max turning angle of the snakes. It is in radians. To convert degrees to radians use: radians=2*pi*(degrees/360)
- Snake generations # heritage: The algorithm uses heritage. Here you can specify the numbers of generations to consider.
- Number of objects to parse: The snakes only see the N closest objects to it's head. Here you specify N.
- Brain init value: Insert a number X. The neural network weights are initialized as random numbers from -X to X.
- Food width: The food width, in pixels.
- Food quantity: the number of food on the screen.
- Points per second: The number of points the snakes gain by second they are alive. (Recommended: 200 to 1000)
- Points per food: The number of points a snake gains by eating one food. (Recommended: 1000 to 3000)
- Points per kill: The number of points a snake gains by killing another snake. (Recommended: <5000)
- Population size: The max number of snakes that the simulation will reach.
- Initial pop. size: The initial number of snakes.
- Pop. increment factor: A number G. Every G generations, the simulation will add one snake to the population.
- Max simulation time: The simulation stops if it reaches 1000 generations, or every snake but one dies, or it passes the maximum simulation time.

How to use:

First of all, set all parameters that you want to change. If one parameter is not entered, the default one will be used. After that, press "Start/Reset".
The simulation will run until it reaches 1000 generations.
If you want to modify a parameter, it's adviced that you first press "Stop", make the changes, the press "Start/Reset".

Tips:

- You may want to start with 4-6 snakes. This way they can first learn how to eat, before crushing one to another.
- After G generations, more snakes will begin to be added. This makes the snakes that previously learnt how to eat, now begin learning how to avoid collision.
- If it is all good, with more snakes the snakes will begin to learn how to kill.

- A high food score will make the snakes more likely to learn how to eat.
- A high time score will make the snakes more likely to survive longer, and avoid collisions.
- A high kill score will make the snakes more likely to learn how to avoid collisions and kill.
- These scores must be balanced: If a snake only knows how to eat, it will die easily by collision; If it only knows how to avoid other snakes, it will eat less;

- A little number of snakes make them more susceptible to learn how to wander around, and how to eat.
- A high number will make them learn how to avoid collisions, but beware: if the snakes haven't learnt how to walk properly, they will die by collision way before they can learn it, that's why you can choose to add snakes by generations.
- A little number of food makes them take more time on how to eat (chase food), but when they do, they do it better.
- A high number of food makes them more likely to learn how to wander around.
- A little number of snakes makes them more susceptible to ignore each other and just learn how to walk and eat.
- A high number of snakes makes them more susceptible to focus on not dying (the time score is important if this is your goal).
