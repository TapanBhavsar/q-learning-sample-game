# Q-learning-sample-game

This project is based on reinforcement learning algorithm which name is Q-learning. In this project, I have created a simple Game.
The game is based on simple falling ball and catching paddle. The ball falling in some speed and it can move left, right or stay. The paddle is steady for every single episode.

Here is three step to run this whole project.

## 1. Install dependancies.

[**Install tensorflow 1.2.1**](https://www.tensorflow.org/versions/r1.2/install/install_linux#InstallingAnaconda) (also need to **install anaconda for python 2.7**)

Install other dependancies:
* install pygame (pip install pygame)
* install keras (pip install keras)
* install numpy (pip install numpy)

## 2. Apply following step to train.

Run command:
```
python rl-network-train.py
```

It will take around **2 to 3 hours** on normal speed GPU

## 3. For Testing accuracy and self-playing game.
Run command:
```
python rl-network-test.py
```

If don't want to train network, get train file from data folder or Just run above testing command.
