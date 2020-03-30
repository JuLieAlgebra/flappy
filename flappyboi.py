import arcade
import numpy as np
from arcade import draw_commands as dc
import flappyengine

####------------CONSTANTS-------------####
DELTA_TIME = 1 # clock unit
SCREEN_VELOCITY = 2.4 + 0.01*DELTA_TIME #pixels/sec
GRAVITY = 0.3 # pixels/sec**

#-------- size of screen ----------------#
screen_height = 1000
screen_width = 1000

class Bird:
    """
    # movement related functions
    # position
    """

    def __init__(self):
        # x, y positions on the screen
        self.x = screen_width / 2.0
        self.y = screen_height / 2.0
        
        # flag for whether or not Player has tapped
        self.jumped = False
        self.flapped = False

        # current y velocity
        self.vel_y = 0 #pixels/sec

        # after key press, reset to the jump velocity
        self.jump_vel = 25 * GRAVITY #pixels/sec

        # visual attributes
        self.radius = 80
        self.texture = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/birb.png")
        self.texture_flapped = self.texture

        #self.texture = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/BirdResting.png")
        #self.texture_flapped = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/BirdFlapped.png")

    def update(self):

        if(self.jumped == True):
            # resets y velocity - FLAP 
            self.vel_y = self.jump_vel
            self.jumped = False

        else:
            # bird is still in free fall
            self.vel_y = self.vel_y - GRAVITY * DELTA_TIME
        
        # updates the position of the bird
        self.y = self.y + self.vel_y



class Pillar:
    """
    ??
    """
    def __init__(self, x = screen_width):

        # left corner of the pillar
        self.x = x

        # y position of the gap, center point of gap
        self.gap = 800

        # width of the pillar
        self.width = 30

        # how big the gap is/height of the gap, should be constant every time
        self.gap_height = 100

        # color of pillars
        self.color = (0, 128, 0) #arcade.csscolor.AO
        self.color_top = (0, 140, 0)

        # flag for whether or not pillar has been passed and counted towards
        # the score
        self.passed = False

        self.texture_bottom = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/ColumnSprite.png")
        self.texture_top = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/ColumnSprite.png", flipped = True)
        self.ground_height = 1/7*screen_height

    def update(self):
        # updates the position of the pillars
        self.x = self.x - SCREEN_VELOCITY

        # we've gone off the screen
        if self.x < 0:

            # creates randomness in the space between pillars
            respawn = np.random.rand(1)

            if respawn >= 0.4:

                # reset the pillar to the end of the screen
                self.x = screen_width

                # randomize where the gap is
                rn = screen_height * np.random.rand(1)
                
                while rn <= self.gap_height/2 + self.ground_height + 10:
                    rn = screen_height * np.random.rand(1)
                
                while rn  >= screen_height - self.gap_height/2 - 1:
                    rn = screen_height * np.random.rand(1)

                self.gap = rn

                self.passed = False


class Game(arcade.Window):
    """
    ??
    """
    def __init__(self):
        # inii tialize the game objects
        self.pillars = None
        
        # initialize a bird
        self.bird = None

        # calls the parent class's init
        super().__init__(screen_width, screen_height)

        # sets background color
        arcade.set_background_color((137, 207, 240))

        # keep track of score
        self.score = 0

        self.ground = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/GrassThinSprite.png")
        self.sky = dc.load_texture("/home/bacon/code/python_toys/flappy/flappyengine/FlappyBirdStyleAssets/Sprites/SkyTileSprite.png")

    def setup(self):
        # initialize the game objects
        self.pillars = [Pillar(0.8 * screen_width), Pillar(screen_width), Pillar(1.4 * screen_width)] 

        # initialize a bird
        self.bird = Bird()

        # reset score to zero
        self.score = 0
        

    def on_key_press(self, key, modifiers):
        self.bird.jumped = True
        self.bird.flapped = True

    def check_collision(self):

        # check for collision with pillars and if we've passed a pillar
        for i in range(len(self.pillars)):
            if (self.pillars[i].x < self.bird.x) and (self.bird.x < self.pillars[i].x + self.pillars[i].width):
                
                if (self.pillars[i].gap - self.pillars[i].gap_height/2 < self.bird.y) and (self.bird.y < self.pillars[i].gap + self.pillars[i].gap_height/2):
                    self.pillars[i].passed = True

                else:
                    self.pillars[i].passed = False
                    # end game, restart
                    self.setup()

            if (self.pillars[i].x + self.pillars[i].width < self.bird.x) and (self.pillars[i].passed):
                self.score = self.score + 1 
                self.pillars[i].passed = False

        # check for falling below the ground
        if self.bird.y < self.pillars[0].ground_height:
            self.setup()


    def update(self, delta):

        for pillar in self.pillars:
            pillar.update()

        # updates the bird
        self.bird.update()

        self.check_collision()


    def on_draw(self):
        """
        Handles drawing the window every time step:
        - Bird
        - Pillars
        - Sky
        - Ground
        Called 1/60 seconds
        
        """

        arcade.start_render()

        self.sky.draw(screen_width/2, screen_height/2, screen_width, screen_height)
        self.ground.draw(screen_width/2, 0.6*self.pillars[0].ground_height, screen_width, self.pillars[0].ground_height)

        # drawing the pillars
        for pillar in self.pillars:

            if pillar.x >= 0:
                 
                ### ---- Top Pillar ----- ###
                arcade.draw_lrtb_rectangle_filled(left = pillar.x, right = pillar.x + pillar.width, 
                    top = screen_height, bottom = pillar.gap + pillar.gap_height / 2, color = pillar.color)
                arcade.draw_lrtb_rectangle_filled(left = pillar.x - 5, right = pillar.x + pillar.width + 5, 
                    top = pillar.gap + pillar.gap_height / 2, bottom = pillar.gap + pillar.gap_height / 2 - 5, color = pillar.color_top)
                
                ### ---- Bottom Pillar ---- ###
                arcade.draw_lrtb_rectangle_filled(left = pillar.x, right = pillar.x + pillar.width, top = pillar.gap - pillar.gap_height / 2,
                    bottom = pillar.ground_height, color = pillar.color)
                arcade.draw_lrtb_rectangle_filled(left = pillar.x - 5, right = pillar.x + pillar.width + 5, top = pillar.gap - pillar.gap_height / 2, 
                    bottom = pillar.gap - pillar.gap_height / 2 - 5, color = pillar.color_top)    

        # draw the bird
        if self.bird.flapped:
            self.bird.texture_flapped.draw(self.bird.x, self.bird.y, self.bird.radius, self.bird.radius)
            self.bird.flapped = False
        else:
            self.bird.texture.draw(self.bird.x, self.bird.y, self.bird.radius, self.bird.radius)
        
        # display the score
        score_display = f"Score: {self.score}"
        arcade.draw_text(score_display, screen_width/3 , 5/6 * screen_height, arcade.csscolor.WHITE, 18)

def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == main():
    main()
