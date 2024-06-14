import pygame
from pygame.locals import *





class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Tennis")

        # CURRENTLY NOT VARIABLE RESOLUTION YET
        self.window_height = 800
        self.window_width = 600

        self.window = pygame.display.set_mode((self.window_height, self.window_width))

        self.player1 = pygame.image.load('C:/Users/miche/Desktop/GAME/img/player1.png')
        self.player2 = pygame.image.load('C:/Users/miche/Desktop/GAME/img/player2.png')
        self.movement1 = [False, False, False, False]  # Left, Right, Up, Down
        self.movement2 = [False, False, False, False]  # Left, Right, Up, Down
        self.p1_pos = [400, 400]
        self.p2_pos = [350, 100]

        self.clock = pygame.time.Clock()
        self.collision_cooldown_p1 = 1000  # 1 second cooldown for player 1
        self.collision_cooldown_p2 = 1000  # 1 second cooldown for player 2
        self.last_collision_time_p1 = 0  # initialize last collision time for player 1
        self.last_collision_time_p2 = 0  # initialize last collision time for player 2
    def run(self):


        # define ball
        ball_obj = pygame.draw.circle(surface=self.window, color=(82, 235, 52), center=[400, 350], radius=7)
        speed = [1, 1] #  [x, y]
        
        running = True
        # Main loop
        while running:

            # draw court (x, y, width, height)
            # pygame.draw.rect(self.window, , (0, 0, 800, 600)) # draw outside court / background (old lol)
            self.window.fill((62, 137, 192)) # fill background
            pygame.draw.rect(self.window, (49, 77, 103), (200, 75, 350, 450)) # draw court
            
            # 10px thick lines
            pygame.draw.rect(self.window, (0, 0, 0), (200, 300, 350, 10)) # draw middle line
            pygame.draw.rect(self.window, (255, 255, 255), (200, 75, 10, 450)) # draw left verical line
            pygame.draw.rect(self.window, (255, 255, 255), (550, 75, 10, 450)) # draw right verical line
            pygame.draw.rect(self.window, (255, 255, 255), (200, 75, 350, 10)) # draw top horizontal line
            pygame.draw.rect(self.window, (255, 255, 255), (200, 515, 350, 10)) # draw bottom horizontal line
            

        
            eventList = pygame.event.get()
            for event in eventList:
                if event.type == pygame.QUIT:
                    running = False
                    break

                # Handle key presses for player 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement1[2] = True
                    if event.key == pygame.K_s:
                        self.movement1[3] = True
                    if event.key == pygame.K_a:
                        self.movement1[0] = True
                    if event.key == pygame.K_d:
                        self.movement1[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement1[2] = False
                    if event.key == pygame.K_s:
                        self.movement1[3] = False
                    if event.key == pygame.K_a:
                        self.movement1[0] = False
                    if event.key == pygame.K_d:
                        self.movement1[1] = False

                # Handle key presses for player 2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement2[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement2[3] = True
                    if event.key == pygame.K_LEFT:
                        self.movement2[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement2[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement2[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement2[3] = False
                    if event.key == pygame.K_LEFT:
                        self.movement2[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement2[1] = False
                    

        

            


            self.p1_pos[0] += (self.movement1[1] - self.movement1[0]) * 3  # Left and Right movement
            self.p1_pos[1] += (self.movement1[3] - self.movement1[2]) * 3  # Up and Down movement

            self.p2_pos[0] += (self.movement2[1] - self.movement2[0]) * 3  # Left and Right movement
            self.p2_pos[1] += (self.movement2[3] - self.movement2[2]) * 3  # Up and Down movement

            # Create rectangles for players
            player1_rect = pygame.Rect(self.p1_pos[0], self.p1_pos[1], self.player1.get_width(), self.player1.get_height())
            player2_rect = pygame.Rect(self.p2_pos[0], self.p2_pos[1], self.player2.get_width(), self.player2.get_height())

            # Blit player images at their updated positions
            self.window.blit(self.player1, self.p1_pos)
            self.window.blit(self.player2, self.p2_pos)

            # # Draw hitboxes for debugging
            # pygame.draw.rect(self.window, (255, 0, 0), player1_rect, 2)  # Red rectangle for player 1
            # pygame.draw.rect(self.window, (0, 255, 0), player2_rect, 2)  # Green rectangle for player 2

            self.p1_pos[0] += (self.movement1[1] - self.movement1[0]) * 0.5  # Left and Right movement1
            self.p1_pos[1] += (self.movement1[3] - self.movement1[2]) * 0.5  # Up and Down movement1

            self.p2_pos[0] += (self.movement2[1] - self.movement2[0]) * 0.5  # Left and Right movement1
            self.p2_pos[1] += (self.movement2[3] - self.movement2[2]) * 0.5  # Up and Down movement1
            
            


            # move the ball
            # Let center of the ball is (100,100)  and the speed is (1,1)
            ball_obj = ball_obj.move(speed)
            # Now center of the ball is (101,101)
            # In this way our wall will move

            self.collision_area = pygame.Rect(50, 50, 350, 50)

            img_r = pygame.Rect(self.p1_pos[0], self.p1_pos[1], self.player1.get_width(), self.player1.get_height())
            
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.window, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.window, (0, 50, 155), self.collision_area)

            # Collision detection with players with cooldown
            current_time = pygame.time.get_ticks()

            def reflect(ball_velocity, normal):
                dot_product = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]
                reflection = [ball_velocity[0] - 2 * dot_product * normal[0], ball_velocity[1] - 2 * dot_product * normal[1]]
                return reflection

            if player1_rect.colliderect(ball_obj):
                if current_time - self.last_collision_time_p1 > self.collision_cooldown_p1:
                    # Determine the collision side and normal vector
                    if player1_rect.collidepoint(ball_obj.centerx, player1_rect.top):
                        normal = [0, -1]  # Top side
                    elif player1_rect.collidepoint(ball_obj.centerx, player1_rect.bottom):
                        normal = [0, 1]  #
                    elif player1_rect.collidepoint(player1_rect.left, ball_obj.centery):
                        normal = [-1, 0]  # Left side
                    elif player1_rect.collidepoint(player1_rect.right, ball_obj.centery):
                        normal = [1, 0]  # Right side

                    # Reflect the ball's speed vector based on the collision normal
                    speed = reflect(speed, normal)

                    # Update the last collision time for player 1
                    self.last_collision_time_p1 = current_time

            if player2_rect.colliderect(ball_obj):
                if current_time - self.last_collision_time_p2 > self.collision_cooldown_p2:
                    # Determine the collision side and normal vector
                    if player2_rect.collidepoint(ball_obj.centerx, player2_rect.top):
                        normal = [0, -1]  # Top side
                    elif player2_rect.collidepoint(ball_obj.centerx, player2_rect.bottom):
                        normal = [0, 1]  # Bottom side
                    elif player2_rect.collidepoint(player2_rect.left, ball_obj.centery):
                        normal = [-1, 0]  # Left side
                    elif player2_rect.collidepoint(player2_rect.right, ball_obj.centery):
                        normal = [1, 0]  # Right side

                    # Reflect the ball's speed vector based on the collision normal
                    speed = reflect(speed, normal)

                    # Update the last collision time for player 2
                    self.last_collision_time_p2 = current_time

            # 200, 75, 350, 450    

            # if ball goes out of screen then change direction of movement1
            if ball_obj.left <= 200 or ball_obj.right >= 550:
                speed[0] = -speed[0]
            if ball_obj.top <= 75 or ball_obj.bottom >= 525:
                speed[1] = -speed[1]

            # draw ball at new centers that are obtained after moving ball_obj
            pygame.draw.circle(surface=self.window, color=(82, 235, 52), center=ball_obj.center, radius=7)

            # update screen
            pygame.display.flip()
            self.clock.tick(75) # 75 FPS
 
        pygame.quit()

Game().run() # run