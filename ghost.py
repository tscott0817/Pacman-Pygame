import pygame
import os
import random
import heapq  # For A* pathfinding
import tracemalloc  # FOR MEMORY PROFILING

class Ghost():
    red_g = os.path.join('assets/img', 'red_ghost.png')
    blue_g = os.path.join('assets/img', 'turquoise_ghost.png')
    yellow_g = os.path.join('assets/img', 'yellow_ghost.png')
    pink_g = os.path.join('assets/img', 'pink_ghost.png')
    scared_g = os.path.join('assets/img', 'scared_ghost.png')
    pygame.mixer.init()  # Not sure best place to put this

    def __init__(self, color):
        if color == "Red":
            self.ghost_img = pygame.image.load(self.red_g).convert_alpha()
            # self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.color = color
        elif color == "Blue":
            self.ghost_img = pygame.image.load(self.blue_g).convert_alpha()
            # self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.color = color
        elif color == "Yellow":
            self.ghost_img = pygame.image.load(self.yellow_g).convert_alpha()
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.color = color
        elif color == "Pink":
            self.ghost_img = pygame.image.load(self.pink_g).convert_alpha()
            # self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.color = color

        # Shared data
        self.red_ghost_img = pygame.image.load(self.red_g).convert_alpha()
        self.blue_ghost_img = pygame.image.load(self.blue_g).convert_alpha()
        self.yellow_ghost_img = pygame.image.load(self.yellow_g).convert_alpha()
        self.pink_ghost_img = pygame.image.load(self.pink_g).convert_alpha()
        self.scared_ghost_img = pygame.image.load(self.scared_g).convert_alpha()
        self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
        self.ghost_bb = pygame.Rect(600, 150, 40, 40)
        self.mouth = pygame.Rect(600, 150, 1, 1)
        self.scared = False
        self.eaten = False
        self.decision = "Start"  # TODO: Doesn't currently do anything with "Start"
        self.speed = 2
        self.chase_switch = 0  # So images are only swapped for one frame
        self.flip_image = 0 # flag to flip the image, 0 to left, 1 to right
        self.scatter_switch = 0

        self.last_timestamp = pygame.time.get_ticks()
        self.frightened_sound = pygame.mixer.Sound("assets/audio/power_pellet.wav")

    def draw(self, window):
        if self.decision == "Right" and self.flip_image == 0:
            self.ghost = pygame.transform.flip(self.ghost, True, False)
            self.flip_image = 1
        if self.flip_image == 1 and self.decision != "Right":
            self.ghost = pygame.transform.flip(self.ghost, True, False)
            self.flip_image = 0

        window.blit(self.ghost, (self.ghost_bb.x, self.ghost_bb.y))
        self.mouth.center = self.ghost_bb.center

    def eat_pacman(self, pacman_obj, pacman_spawn):
        if self.mouth.colliderect(pacman_obj):
            # pygame.time.delay(1000)
            pacman_obj.center = pacman_spawn.center
            return True
        else:
            return False

        # if self.mouth.colliderect(pacman_obj):
        #     self.ghost = pygame.transform.scale(self.ghost, (120, 120))
        #     self.bigger = 1
        #     pygame.time.delay(1000)
        #     pacman_obj.center = pacman_spawn.center
        #     return True
        # else:
        #     self.bigger = 0
        #     self.ghost = pygame.transform.scale(self.ghost, (40, 40))
        #     return False

    # def chase(self, decision_nodes, pacman):
    #     if self.color == "Blue" and self.chase_switch == 0:
    #         self.ghost_img = self.blue_ghost_img
    #         self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
    #         self.chase_switch = 1
    #     elif self.color == "Red" and self.chase_switch == 0:
    #         self.ghost_img = self.red_ghost_img
    #         self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
    #         self.chase_switch = 2
    #     elif self.color == "Yellow" and self.chase_switch == 0:
    #         self.ghost_img = self.yellow_ghost_img
    #         self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
    #         self.chase_switch = 3
    #     elif self.color == "Pink" and self.chase_switch == 0:
    #         self.ghost_img = self.pink_ghost_img
    #         self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
    #         self.chase_switch = 4
    #
    #     decision_made = False
    #     available_directions = []  # All possible traversal directions, to be filled as decisions are made
    #
    #     # Find the closest decision node to the pacman
    #     closest_node = min(decision_nodes, key=lambda node: self.calculate_distance(node, pacman))  # TODO: Just getting closest to Pacman could lead to wrong nodes (like on opposite sides of walls)
    #
    #     # Check if the ghost is at a decision node
    #     if self.ghost_bb.center in decision_nodes:
    #         print("Ghost at decision node")
    #         # Clear available directions when at a decision node
    #         available_directions = []
    #
    #         # Calculate distances from the ghost to all decision nodes using A* algorithm
    #         distances = {}
    #         for node in decision_nodes:
    #             distances[(node[0], node[1])] = float('inf')
    #         distances[self.ghost_bb.center] = 0
    #         queue = [(0, self.ghost_bb.center)]
    #
    #         while queue:
    #             dist, current_node = heapq.heappop(queue)
    #
    #             if dist > distances[(current_node[0], current_node[1])]:
    #                 continue
    #
    #             # Check if the ghost has reached the closest decision node
    #             if current_node == closest_node:
    #                 break
    #
    #             for neighbor in decision_nodes:
    #                 if current_node != neighbor:
    #                     new_dist = dist + self.calculate_distance(current_node, neighbor)
    #                     if new_dist < distances[(neighbor[0], neighbor[1])]:
    #                         distances[(neighbor[0], neighbor[1])] = new_dist
    #                         heapq.heappush(queue, (new_dist, neighbor))
    #
    #         for neighbor in decision_nodes:
    #             if self.ghost_bb.center != neighbor:
    #                 if self.ghost_bb.y == neighbor.y and self.ghost_bb.x > neighbor.x and "Left" not in available_directions:
    #                     available_directions.append("Left")
    #                 if self.ghost_bb.y == neighbor.y and self.ghost_bb.x < neighbor.x and "Right" not in available_directions:
    #                     available_directions.append("Right")
    #                 if self.ghost_bb.x == neighbor.x and self.ghost_bb.y < neighbor.y and "Down" not in available_directions:
    #                     available_directions.append("Down")
    #                 if self.ghost_bb.x == neighbor.x and self.ghost_bb.y > neighbor.y and "Up" not in available_directions:
    #                     available_directions.append("Up")
    #
    #         decision_made = True
    #
    #     # # Check if the ghost is at a decision node and a path is available
    #     # if decision_made and len(available_directions) > 0:
    #     #     # If more than one path has the same distance (like at the game start), choose one at random
    #     #     # Otherwise, the list has only one item so it will always be picked
    #     #     choice = random.randint(0, len(available_directions) - 1)
    #     #     self.decision = available_directions[choice]
    #     #     available_directions = []  # Clear available directions after making a decision
    #
    #     # Now move the ghost in the chosen direction
    #     if decision_made:
    #         if self.decision == "Start":
    #             self.ghost_bb.y -= self.speed
    #         elif self.decision == "Left":
    #             self.ghost_bb.x -= self.speed
    #         elif self.decision == "Right":
    #             self.ghost_bb.x += self.speed
    #         elif self.decision == "Up":
    #             self.ghost_bb.y -= self.speed
    #         elif self.decision == "Down":
    #             self.ghost_bb.y += self.speed
    #     elif not decision_made:
    #         print("The ghost can't find a direction to travel! Check that the board layout is fully connected.")
    #
    # # Helper method to calculate the distance between two points
    # def calculate_distance(self, point1, point2):
    #     x1 = point1[0]
    #     y1 = point1[1]
    #     x2 = point2[0]
    #     y2 = point2[1]
    #     return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


    # TODO: Old chase method
    # The ghost chases Pacman
    def chase(self, decision_nodes, pacman):
        if self.color == "Blue" and self.chase_switch == 0:
            self.ghost_img = self.blue_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.chase_switch = 1
        elif self.color == "Red" and self.chase_switch == 0:
            self.ghost_img = self.red_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.chase_switch = 2
        elif self.color == "Yellow" and self.chase_switch == 0:
            self.ghost_img = self.yellow_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.chase_switch = 3
        elif self.color == "Pink" and self.chase_switch == 0:
            self.ghost_img = self.pink_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.chase_switch = 4

        decision_made = False
        available_directions = []  # All possible traversal directions, to be filled as decisions are made
        center_count = 0  # Used for stopping if statement after one frame when the node that the ghost is at is found

        # First check all the decision nodes for the ghost.
        for current_node in decision_nodes:
            # Is the ghost at a decision node?
            if self.ghost_bb.center == current_node.center and center_count == 0:
                # Get all possible travel directions for ghost
                for next_node in decision_nodes:
                    # Allow travel left if node exists to the left of current node
                    # Same for all other directions, relative to direction
                    if current_node.y == next_node.y and current_node.x > next_node.x and "Left" not in available_directions:
                        # Choose direction closest to Pacman position and distance.
                        # Same for all other choices, relative to position
                        if self.ghost_bb.x > pacman.x:
                            available_directions.append("Left")
                    # TODO: Can't remember if the (-20) and (+20) are needed
                    if current_node.y == next_node.y and current_node.x < next_node.x and "Right" not in available_directions:
                        if self.ghost_bb.x < pacman.x:
                            available_directions.append("Right")
                    if current_node.x == next_node.x and current_node.y < next_node.y and "Down" not in available_directions:
                        if self.ghost_bb.y < pacman.y:
                            available_directions.append("Down")
                    if current_node.x == next_node.x and current_node.y > next_node.y and "Up" not in available_directions:
                        if self.ghost_bb.y > pacman.y:
                            available_directions.append("Up")

                center_count = 1  # Set to one so if check stops executing after the first math is found

            decision_made = True  # Once at this point a can be made


        # Print available directions

        # If more than one path has the same distance (like at the game start), choose one at random
        # Otherwise the list has only one item so it will always be picked
        if len(available_directions) > 0:
            print(available_directions)
            choice = random.randint(0, len(available_directions) - 1)
            self.decision = available_directions[choice]

        # Now move the ghost in the chosen direction
        if decision_made:
            if self.decision == "Start":
                self.ghost_bb.y -= self.speed
            elif self.decision == "Left":
                self.ghost_bb.x -= self.speed
            elif self.decision == "Right":
                self.ghost_bb.x += self.speed
            elif self.decision == "Up":
                self.ghost_bb.y -= self.speed
            elif self.decision == "Down":
                self.ghost_bb.y += self.speed
        elif not decision_made:
            print("The ghost can't find a direction to travel! Check that the board layout is fully connected.")

    # When ghost is running from Pacman
    # TODO: Sometimes picks non-traversable paths
    def playSound(self, sound, wait_time):
        # If 1 second has passed since last time stamp, play chomp audio
        current_time = pygame.time.get_ticks()
        if current_time - self.last_timestamp >= wait_time:
            pygame.mixer.Sound.play(sound)
            pygame.mixer.music.stop()
            self.last_timestamp = current_time
    def frightened(self, decision_nodes, pacman):
        # self.playSound(self.frightened_sound, 1000)

        # Swap image
        if self.scared and self.chase_switch == 1 or self.chase_switch == 2 or self.chase_switch == 3 or self.chase_switch == 4\
                       or self.scatter_switch == 1 or self.scatter_switch == 2 or self.scatter_switch == 3 or self.scatter_switch == 4:
            self.ghost = pygame.transform.scale(self.scared_ghost_img, (40, 40))
            self.chase_switch = 0
            self.scatter_switch = 0

        decision_made = False
        available_directions = []  # All possible traversal directions, to be filled as decisions are made
        center_count = 0  # Used for stopping if statement after one frame when the node that the ghost is at is found

        # First check all the decision for the ghost.
        for current_node in decision_nodes:
            # Is the ghost at a decision node?
            if self.ghost_bb.center == current_node.center and center_count == 0:
                # Get all possible travel directions for ghost
                for next_node in decision_nodes:
                    # If y-value matches another node, and there exista a node to the left of the current node x-value, then allow left turn
                    if current_node.y == next_node.y and current_node.x > next_node.x and "Left" not in available_directions:
                        if self.ghost_bb.x < pacman.x:
                            available_directions.append("Left")
                    if current_node.y == next_node.y and current_node.x < next_node.x - 20 and "Right" not in available_directions:
                        if self.ghost_bb.x > pacman.x:
                            available_directions.append("Right")
                    if current_node.x == next_node.x and current_node.y < next_node.y and "Down" not in available_directions:
                        if self.ghost_bb.y > pacman.y:
                            available_directions.append("Down")
                    if current_node.x == next_node.x and current_node.y > next_node.y + 20 and "Up" not in available_directions:
                        if self.ghost_bb.y < pacman.y:
                            available_directions.append("Up")
                    else:
                        available_directions.append("Up")
                        available_directions.append("Down")
                        available_directions.append("Left")
                        available_directions.append("Right")

                center_count = 1  # Set to one so if check stops executing after the first math is found

            decision_made = True  # Once at this point a can be made

        # If more than one path has the same distance (like at the game start), choose one at random
        # Otherwise the list has only one item so it will always be picked
        if len(available_directions) > 0:
            choice = random.randint(0, len(available_directions) - 1)
            self.decision = available_directions[choice]

        # Now move the ghost in the chosen direction
        if decision_made:
            if self.decision == "Start":
                self.ghost_bb.y -= self.speed
            elif self.decision == "Left":
                self.ghost_bb.x -= self.speed
            elif self.decision == "Right":
                self.ghost_bb.x += self.speed
            elif self.decision == "Up":
                self.ghost_bb.y -= self.speed
            elif self.decision == "Down":
                self.ghost_bb.y += self.speed
        elif not decision_made:
            print("The ghost can't find a direction to travel! Check that the board layout is fully connected.")

    # Move in random directions
    def scatter(self, decision_nodes):
        if self.color == "Blue" and self.scatter_switch == 0:
            self.ghost_img = self.blue_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.scatter_switch = 1
        elif self.color == "Red" and self.scatter_switch == 0:
            self.ghost_img = self.red_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.scatter_switch = 1
        elif self.color == "Yellow" and self.scatter_switch == 0:
            self.ghost_img = self.yellow_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.scatter_switch = 1
        elif self.color == "Pink" and self.scatter_switch == 0:
            self.ghost_img = self.pink_ghost_img
            self.ghost = pygame.transform.scale(self.ghost_img, (40, 40))
            self.scatter_switch = 1

        decision_made = False
        available_directions = []  # All possible traversal directions, to be filled as decisions are made
        center_count = 0  # Used for stopping if statement after one frame when the node that the ghost is at is found

        # First check all the decision nodes for the ghost.
        for current_node in decision_nodes:
            # Is the ghost at a decision node?
            if self.ghost_bb.center == current_node.center and center_count == 0:
                # Get all possible travel directions for ghost
                for next_node in decision_nodes:
                    # If y-value matches another node, and there exista a node to the left of the current node x-value, then allow left turn
                    if current_node.y == next_node.y and current_node.x > next_node.x and "Left" not in available_directions:
                        available_directions.append("Left")
                    if current_node.y == next_node.y and current_node.x < next_node.x - 20 and "Right" not in available_directions:
                        available_directions.append("Right")
                    if current_node.x == next_node.x and current_node.y < next_node.y and "Down" not in available_directions:
                        available_directions.append("Down")
                    if current_node.x == next_node.x and current_node.y > next_node.y + 20 and "Up" not in available_directions:
                        available_directions.append("Up")

                center_count = 1  # Set to one so if check stops executing after the first match is found

            decision_made = True  # Once at this point a can be made

        # Re-write the above for loop with only one loop
        # for i, current_node in enumerate(decision_nodes):



        # If more than one path has the same distance (like at the game start), choose one at random
        # Otherwise the list has only one item so it will always be picked
        if len(available_directions) > 0:
            choice = random.randint(0, len(available_directions) - 1)
            self.decision = available_directions[choice]

        # Now move the ghost in the chosen direction
        if decision_made:
            if self.decision == "Start":
                self.ghost_bb.y -= self.speed
            elif self.decision == "Left":
                self.ghost_bb.x -= self.speed
            elif self.decision == "Right":
                self.ghost_bb.x += self.speed
            elif self.decision == "Up":
                self.ghost_bb.y -= self.speed
            elif self.decision == "Down":
                self.ghost_bb.y += self.speed
        elif not decision_made:
            print("The ghost can't find a direction to travel! Check that the board layout is fully connected.")

