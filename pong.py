import random
import pygame

class Pong:
    
    def __init__(self):
        '''This initializes the the game object and screen '''
        
        pygame.init()
        self.screen_height = 750
        self.screen_width = 1250
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.player1_pos = pygame.Vector2(80, self.screen_height - 80)
        self.player2_pos = pygame.Vector2(self.screen_width - 40, self.screen_height - 80)
        
    
    def draw(self,paddle,ball):
        '''This deals with the drawing of the items onto the screen. In future
        versions I want to add a sort of home screen where the player can choose
        to play with a computer or person, and also a scoreboard in the game.'''
        
        self.screen.fill('black')
        paddle.draw(self.screen)
        ball.draw(self.screen)
               
        
    
    def update(self):
        '''This is the constant updating of the game '''
        
        pygame.display.flip()
        self.clock.tick(60)
        
    
    def play(self):
        '''This deals with the actual game loop itself: This method
        refers to the all the other methods and deals with them. The screen automatically gets 
        initialized above but here we are going to deal with the screen method and then run
        the game loop'''
        
        game_running = True
        paddles = Paddle(2)
        game_ball = Ball()
        while game_running:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False            
            self.draw(paddles,game_ball)
            paddles.move()
            game_ball.move(paddles)
            game_ball.ballreset()
            self.update()
        pygame.quit()
            
            
        
    
class Paddle:
    
    def __init__(self,players):
        '''Deals with initializing of paddles and probably drawing of paddles
        as well, we'll see'''
        
        self.players = players
        self.screen_height = 750
        self.screen_width = 1250
        self.player1_pos = [80, (self.screen_height/2) - 80]
        self.player2_pos = [self.screen_width - 80, (self.screen_height/2) - 80]        
        #self.paddle1 = pygame.Rect(self.player1_pos[0],self.player1_pos[1], 20, 120)
        #self.paddle2 = pygame.Rect(self.player2_pos[0],self.player2_pos[1], 20, 120)
        
    
    def draw(self,screen): 
        '''Deals with the drawing of the paddles'''
        
        self.paddle1 = pygame.Rect(self.player1_pos[0],self.player1_pos[1], 20, 120)
        self.paddle2 = pygame.Rect(self.player2_pos[0],self.player2_pos[1], 20, 120)            
        pygame.draw.rect(screen, 'white', self.paddle1)
        pygame.draw.rect(screen, 'white', self.paddle2)
                       
                          
        
    def move(self):
        '''Deals with the movement of the paddles. I want to improve this method
        by adding some sort of one player vs computer functionality so you can
        play by yourself. I think I'm going to try that by making the
        computer paddle follow the y-position of the ball once it crosses into
        its half of the screen'''
    
        if self.players == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player1_pos[1] -= 7
                if self.player1_pos[1] <= 0:
                    self.player1_pos[1] = 0               
                
            if keys[pygame.K_s]:
                self.player1_pos[1] += 7
                if self.player1_pos[1] >= (self.screen_height-120):
                    self.player1_pos[1] = (self.screen_height-120)                 
                
            
      
        '''This is for the option if a player wants to play with another player'''
        
        # This method tests whether a certain key is pressed, and if true,
        # increment the position of the paddle in the y-direction by a 
        # predetermined speed value.
        
        if self.players == 2:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player1_pos[1] -= 7 
                if self.player1_pos[1] <= 0:
                    self.player1_pos[1] = 0                 
            if keys[pygame.K_s]:
                self.player1_pos[1] += 7
                if self.player1_pos[1] >= (self.screen_height-120):
                    self.player1_pos[1] = (self.screen_height-120)                
            if keys[pygame.K_i]:
                self.player2_pos[1] -= 7
                if self.player2_pos[1] <= 0:
                    self.player2_pos[1] = 0                 
            if keys[pygame.K_k]:
                self.player2_pos[1] += 7 
                if self.player2_pos[1] >= (self.screen_height-120):
                    self.player2_pos[1] = (self.screen_height-120)                
                       
        
        
    
    
class Ball:
    def __init__(self):
        '''Deals with initializing of the ball and drawing as well most likely '''
        self.screen_height = 750
        self.screen_width = 1250         
        self.pos = [self.screen_width / 2, self.screen_height / 2]
        self.ball_speed_x = 7
        self.ball_speed_y = 7
        
    
    def draw(self,screen):
        '''Deals with drawing of the ball for now '''
        self.ball = pygame.draw.circle(screen,'white', self.pos, 20)
        
        
    
    def move(self, paddles):
        '''Deals with the movement of the ball'''
        
        # These lines of code increment the position of the ball by a 
        # predetermined speed value and also calls the bounce method.
        
        self.pos[0] += self.ball_speed_x
        self.pos[1] += self.ball_speed_y
        self.bounce(paddles)
              
        
        
    
    def bounce(self, paddles):
        '''Deals with the bouncing of the ball off walls and paddles '''
        
        # The first part of this code deals with the bouncing of the ball off the
        # walls. It does so by testing to see if the y-coordinate of the ball is
        # either less than its radius of 20, meaning it is out of the top bound,
        # or greater than the height of the screen minus the radius, meaning it
        # is out of the lower bound of the screen.
        
        if self.pos[1] <= 20:
            self.ball_speed_y *= -1
        if self.pos[1] >= 730:
            self.ball_speed_y *= -1
            
        # This next part of the code deals with the bouncing of the ball off the
        # paddles. It checks for two statements, and if they are true, they 
        # bounce the ball backward. The first statement checks if the distance
        # between the x-coordinate of the ball and the the x coordinate of the 
        # paddles are between a certain distance, and if true, check to see if 
        # the y-coordinate of the ball is in between the length of the paddle.
        # There is a little bug that occured where the ball would bounce through
        # the length of the paddle and bounce behind the paddle so thats where 
        # the '30 <=' and '10 <=' conditions came from, which eliminated the
        # issue of the ball bouncing behind the paddle and also drastically
        # reduced the issue of the ball bouncing through the length of the 
        # paddle.
        
        if 30 <= (self.pos[0] - paddles.player1_pos[0])  <= 40:
            if self.pos[1] >= paddles.player1_pos[1] and self.pos[1] <= (paddles.player1_pos[1] + 120):
                self.ball_speed_x *= -1
        if 10 <= (paddles.player2_pos[0] - self.pos[0])  <= 20:
            if self.pos[1] >= paddles.player2_pos[1] and self.pos[1] <= (paddles.player2_pos[1] + 120):
                self.ball_speed_x *= -1        
            
    def ballreset(self):
        '''Resets the ball to its original position if it goes out of bounds'''
        
        # This code tests if the x-coordinate of the ball is either less than 
        # zero or greater than the width of the screen, and if so, return the 
        # ball to its original position
        
        if self.pos[0] <= 20 or self.pos[0] >= (self.screen_width - 20):
            self.pos = [self.screen_width / 2, self.screen_height / 2]
            self.ball_speed_x *= -1 
        
            
        
        
    
    
def main():
    new_game = Pong()
    new_game.play()
    
main()