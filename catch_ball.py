import os
import numpy as np


class CatchBall:
    def __init__(self):
        # parameters
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.screen_n_rows = 12
        self.screen_n_cols = 12
        self.player_length = 1
        self.enable_actions = (0, 1, 2, 3, 4)
        self.frame_rate = 10

        # variables
        self.reset()

    def update(self, action):
        """
        action:
            // 0: do nothing
            1: move left
            2: move right
            3: move up
            4: move down
        """
        # update player position
        if action == self.enable_actions[1]:
            # move left
            self.player_col = max(0, self.player_col - 1)
        elif action == self.enable_actions[2]:
            # move right
            self.player_col = min(self.player_col + 1, self.screen_n_cols - self.player_length)
        elif action == self.enable_actions[3]:
            # move up
            self.player_row = max(self.player_row - 1, 0)
        elif action == self.enable_actions[4]:
            # move down
            self.player_row = min(self.player_row + 1, self.screen_n_cols - self.player_length)
        else:
            # do nothing
            pass

        # update ball position
        # *** ball never moves ***
        # self.ball_row = min(self.ball_row + 1, self.screen_n_rows - 1);

        # collision detection
        self.reward = 0
        self.terminal = False

        self.counter += 1

        # print(c)
        if self.player_col == self.screen_n_cols - self.player_length and self.player_row == self.screen_n_rows - self.player_length:
            # catch
            self.counter = 0

            self.terminal = True
            self.reward = 1
        else:
            # drop
            a = self.player_col 
            b = self.player_row 
            distance_to_goal = pow(self.screen_n_cols - a - 1, 2) + pow(self.screen_n_rows - b - 1, 2)
            if self.last_distance > distance_to_goal:
                self.last_distance = distance_to_goal
                self.reward = 1
            else:
                self.reward = -1

        # print(self.reward)
        if self.counter == 24:
            self.counter = 0
            self.reward = -1
            self.terminal = True

    def draw(self):
        # reset screen
        self.screen = np.zeros((self.screen_n_rows, self.screen_n_cols))

        # draw player
        for i in range(self.player_length):
            self.screen[self.player_row+i, self.player_col:self.player_col + self.player_length] = 1

        # draw ball
        # self.screen[self.ball_row, self.ball_col] = 1

    def observe(self):
        self.draw()
        return self.screen, self.reward, self.terminal

    def execute_action(self, action):
        self.update(action)

    def reset(self):
        # reset player position
        self.player_row = np.random.randint(self.screen_n_rows - self.player_length)
        self.player_col = np.random.randint(self.screen_n_cols - self.player_length)
        # self.player_row = 0
        # self.player_col = 0 

        # reset ball position
        # self.ball_row = np.random.randint(self.screen_n_rows)
        # self.ball_col = np.random.randint(self.screen_n_cols)

        # reset other variables
        self.reward = 0
        self.terminal = False
        self.counter = 0
        self.last_distance = 200
