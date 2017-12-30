# -*- coding: utf-8 -*-
from __future__ import division, print_function

import collections
import numpy as np
import pygame
import random
import os

# creating class for Game
class MyWrappedGame(object):
    
    def __init__(self):        
        pygame.init()
        pygame.key.set_repeat(10, 100)
        
        # set constants
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_BLACK = (0, 0, 0)

        # frame size of game
        self.GAME_WIDTH = 400
        self.GAME_HEIGHT = 400

        # Moving ball size
        self.BALL_WIDTH = 20
        self.BALL_HEIGHT = 20

        # steady paddle size
        self.PADDLE_WIDTH = 50
        self.PADDLE_HEIGHT = 10
        self.GAME_FLOOR = 350
        self.GAME_CEILING = 10

        # ball droping velocity in pixels/sec
        self.BALL_VELOCITY = 10

        # ball right left movement velocity in pixels/sec
        self.BALL_MOVEMENT_VELOCITY = 20

        # if we want to print current status on game
        self.FONT_SIZE = 30
        self.MAX_TRIES_PER_GAME = 1
        self.CUSTOM_EVENT = pygame.USEREVENT + 1
        self.font = pygame.font.SysFont("Comic Sans MS", self.FONT_SIZE)
        
    # Reset function initialize after every episode
    def reset(self):
        self.frames = collections.deque(maxlen=4)
        self.game_over = False
        # initialize random position of paddle
        self.paddle_x = random.randint(0, self.GAME_WIDTH - self.PADDLE_WIDTH)#self.GAME_WIDTH // 2
        self.game_score = 0
        self.reward = 0
        # initialize random poistion of ball
        self.ball_x = random.randint(0, self.GAME_WIDTH)
        self.ball_y = self.GAME_CEILING
        self.num_tries = 0
        # set up display, clock, etc
        self.screen = pygame.display.set_mode(
                (self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
    
    def step(self, action):
        pygame.event.pump()
        
        if action == 0:   # move ball left
            self.ball_x -= self.BALL_MOVEMENT_VELOCITY
            if self.ball_x < 0:
                # bounce off the wall, go right
                self.ball_x = self.BALL_MOVEMENT_VELOCITY
        elif action == 2: # move ball right
            self.ball_x += self.BALL_MOVEMENT_VELOCITY
            if self.ball_x > self.GAME_WIDTH - self.BALL_WIDTH:
                # bounce off the wall, go left
                self.ball_x = self.GAME_WIDTH - self.BALL_WIDTH - self.BALL_MOVEMENT_VELOCITY
        else:             # dont move ball
            pass

        # Create background black
        self.screen.fill(self.COLOR_BLACK)

        # If we want to print status in game pls uncomment below 4 lines
        # score_text = self.font.render("Score: {:d}/{:d}, Ball: {:d}".format(self.game_score, self.MAX_TRIES_PER_GAME, self.num_tries), True, self.COLOR_WHITE)
        # self.screen.blit(score_text, 
        #    ((self.GAME_WIDTH - score_text.get_width()) // 2,
        #     (self.GAME_FLOOR + self.FONT_SIZE // 2)))
                
        # update ball position
        self.ball_y += self.BALL_VELOCITY
        ball = pygame.draw.rect(self.screen, self.COLOR_WHITE, pygame.Rect(self.ball_x, self.ball_y, self.BALL_WIDTH, self.BALL_HEIGHT))
        # update paddle position
        paddle = pygame.draw.rect(self.screen, self.COLOR_WHITE, pygame.Rect(self.paddle_x, self.GAME_FLOOR, self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        
        # check for collision and update reward
        self.reward = 0
        if self.ball_y >= self.GAME_FLOOR - self.BALL_WIDTH // 2:
            if ball.colliderect(paddle):
                self.reward = 1
            else:
                self.reward = -1
                
            self.game_score += self.reward
            self.ball_x = random.randint(0, self.GAME_WIDTH)
            self.ball_y = self.GAME_CEILING
            self.num_tries += 1
            
        pygame.display.flip()
            
        # save last 4 frames
        self.frames.append(pygame.surfarray.array2d(self.screen))
        
        if self.num_tries >= self.MAX_TRIES_PER_GAME:
            self.game_over = True
            
        self.clock.tick(30)
        return self.get_frames(), self.reward, self.game_over
        

    def get_frames(self):
        return np.array(list(self.frames))
    

# main function for testing, is game is working or not
if __name__ == "__main__":   
    game = MyWrappedGame()

    NUM_EPOCHS = 10
    for e in range(NUM_EPOCHS):
        print("Epoch: {:d}".format(e))
        game.reset()
        input_t = game.get_frames()
        game_over = False
        while not game_over:
            action = np.random.randint(0, 3, size=1)[0]
            input_tp1, reward, game_over = game.step(action)
            print(action, reward, game_over)
