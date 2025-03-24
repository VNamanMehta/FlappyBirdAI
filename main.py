import neat.config
import neat.nn.feed_forward
import pygame
import neat
import time
import os
import random

pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 750

#Load the bird images along with scaling them to 2x
B1 = pygame.image.load(os.path.join("imgs","bird1.png"))
B2 = pygame.image.load(os.path.join("imgs","bird2.png"))
B3 = pygame.image.load(os.path.join("imgs","bird3.png"))
BIRD_IMAGES = [pygame.transform.scale2x(B1),
               pygame.transform.scale2x(B2),
               pygame.transform.scale2x(B3)]

#Load the pipe images along with scaling them to 2x
PIPE_IMAGE = pygame.image.load(os.path.join("imgs","pipe.png"))
PIPE_IMAGE = pygame.transform.scale2x(PIPE_IMAGE)

#Load the base image along with scaling it to 2x
BASE_IMAGE = pygame.image.load(os.path.join("imgs","base.png"))
BASE_IMAGE = pygame.transform.scale2x(BASE_IMAGE)

#Load the background image along with scaling it to 2x
BG_IMAGE = pygame.image.load(os.path.join("imgs","bg.png"))
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5 #Time to show each bird image (in game frames)

    def __init__(self,x,y):
        self.x = x #Initial x (horizontal) position
        self.y = y #Initial y (vertical) position
        self.tilt = 0 #Initial tilt of the bird (degree of change in angle when moving up and down)
        self.tick_count = 0 #Initial tick count to keep track of the acceleration due to gravity (jump and fall down)
        self.vel = 0 #Initial velocity of the bird
        self.height = self.y #Initial height of the bird (point where it was before the jump) (also to track how much the bird has moved relative to the starting point after jump)
        self.img_count = 0 #counter that shows different bird images based on the multiples of the animation time
        self.img = self.IMGS[0]

    '''
    In pygame, the origin (0,0) is at the top left corner of the window. The x-axis is horizontal and the y-axis is vertical.
    The bird moves up when the y-coordinate decreases and moves down when the y-coordinate increases.
    The bird moves right when the x-coordinate increases and moves left when the x-coordinate decreases.
    And when we jump we want the bird to move up and when we don't jump we want the bird to move down.
    '''

    def jump(self):
        self.vel = -10.5 #Negative velocity to move up
        self.tick_count = 0 #Reset the tick count after jump. Resetting tick_count = 0 ensures gravity starts fresh after each jump.
        self.height = self.y #Reset the height after jump.Tracks how far the bird has traveled since jumping.

    def move(self):
        self.tick_count += 1 #Increment the tick count after each frame
        
        '''
        eq1 => self.vel * self.tick_count => Since self.vel is negative and self.tick_count is positive, the product is negative. This means the bird will move up.
        eq2 => 1.5 * self.tick_count**2 => Since ticket_count is positive keeps increasing, the product is also positive.
        When we add the both eq1 and eq2, the bird will move up and then fall down due to gravity.(As initially eq1 is negative and eq2 is positive and |eq1| > |eq2| the sum is negative and bird moves up.
         But as the ticket_count increases, the sum will become positive and the bird will fall down due to gravity.)  
        '''
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2 #Calculate the displacement of the bird based on the current velocity and the time elapsed

        if d>=16: #Terminal velocity
            d = 16 #If the bird is moving down with a velocity greater than 16 (since d value keeps increasing as it falls down), set the velocity to 16. Prevents the bird from falling too fast.

        if d < 0: #If the bird is moving up
            d-=2 #Move the bird up a little more (to make the jump look more natural)(fine-tuning the jump)

        self.y += d #Update the y-coordinate of the bird based on the displacement calculated above

        if d < 0 or self.y < self.height + 50:
            ''''
            d<0 => If the bird is moving up
            self.y < self.height + 50 => self.y
            Since self.y is the current y-coordinate of the bird and self.height is the initial y-coordinate of the bird before the jump,
            and since negaive means up and positive means down,
            lesser value means up and greater value means down.
            So, self.y < self.height means the bird is above the starting point of the jump.
            We add 50 to self.height to give it some buffer space to make the jump look more natural.
            That is if the bird is within 50px range(below as well) of the starting point of the jump, we still want the bird to tilt up.
            '''
            if self.tilt < self.MAX_ROTATION: #If the bird is not tilted at the maximum angle
                self.tilt = self.MAX_ROTATION #Tilt the bird to the maximum angle
        else:
            if self.tilt > -90: #The bird is falling down and the bird is not facing vertically downwards
                self.tilt -= self.ROT_VEL #Gradually tilt the bird to face vertically downwards and stop tilting when it reaches -90 degrees i.e., vertically downwards.
                # Else the bird will keep tilting beyond -90 degrees and make it upside down.

    def draw(self,window):
        self.img_count += 1 # increase the image count to show different bird images based on the multiples of the animation time

        '''
        Inefficient way of showing bird images based on the multiples of the animation time.
        Total number of frames shown per bird flapping cycle (since animation time is 5):
        frames 0-4 => bird1.png
        frames 5-9 => bird2.png
        frames 10-14 => bird3.png
        frames 15-19 => bird2.png
        frames 20-21 => bird1.png (reset the animation cycle)
          if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        '''

        #Efficient way of showing bird images based on the multiples of the animation time.
        '''
        self.ANIMATION_TIME*4 + 1 = 21, total number of frames per cycle of bird flapping (since animation time is 5)
        self.img_count + 1 increaments the img_count by 1 and takes the remainder when divided by self.ANIMATION_TIME*4 + 1 
        Hence img_count goes from 1 to 21 and then reset to 1.
        '''
        self.img_count = (self.img_count + 1) % (self.ANIMATION_TIME*4 + 1)
        '''
        frame_index = self.img_count // self.ANIMATION_TIME gives the values => for frames 0-4 => 0, for frames 5-9 => 1,
        for frames 10-14 => 2, for frames 15-19 => 3, for frames 20-21 => 4,
        but we need a loop of 0,1,2,1,0 to show the bird flapping animation.
        hence we use frame_order = [0,1,2,1,0] to get the required loop.
        frame_order[frame_index] gives the required loop of 0,1,2,1,0 eg: for frame_index 0, frame_order[0] = 0, for frame_index 1, frame_order[1] = 1, 
        for frame_index 2, frame_order[2] = 2, for frame_index 3, frame_order[3] = 1, for frame_index 4, frame_order[4] = 0
        '''
        frame_index = self.img_count // self.ANIMATION_TIME
        frame_order = [0,1,2,1,0]
        self.img = self.IMGS[frame_order[frame_index]]

        if self.tilt <= -80: #If the bird is facing vertically downwards we dont want it to flap its wings
            self.img = self.IMGS[1] #Set the bird image to the middle image (bird2.png)
            self.img_count = self.ANIMATION_TIME*2 #Set the image count to 10 since after frames 5-9 we have to show the bird2.img and keep it as bird1.png it self.

        '''
        Rotate the image (self.img) by self.tilt degrees counterclockwise.
        The rotated image may have a different size (bounding box expands).
        Rotation happens around the top-left corner by default, which we need to fix.
        Thus first we get the bounding box of the self.img.get_rect(topleft=(self.x,self.y)) => this aligns the topleft of the rectangle(bounding box) to the topleft of the image.
        Then we get the center of the bounding box using .center => this is the point around which we will rotate the image.(as we want to rotate the image around the center)
        Now the rotated image needs a new bounding box whose center is aligned with the center of the bounding box of the original image(self.img.get_rect()).
        This is because the rotated image and the original image will have different dimensions, size and centers.
        Therefore we align them by explicitly setting the center of the rotated image to the center of the original image. 
        '''
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center) #self.x and self.y are the topleft conrners of the original image
        #The position of the rect is based on the center of the rotated image (whose center is calculated from the center of the original image)
        window.blit(rotated_image, new_rect.topleft) #Draw the rotated image on the window at the new_rect.topleft position.

    def get_mask(self):
        return pygame.mask.from_surface(self.img) #creates a mask around the bird (2D bit mask or binary representation) to check for pixel perfect collisions.
        

class Pipe:
    GAP = 200 #Defines the vertical space between the top and bottom pipes.
    VEL = 5 #Velocity of the pipes moving towards the bird

    def __init__(self, x): # we are not passing y because the y-coordinate (height) of the pipes will be randomly generated
        self.x = x #Stores the horizontal position of the pipes. The pipes start at a certain position on the right (x coordinate) and move left over time.
        self.height = 0 #Stores the randomly generated height of the pipes.
        self.top = 0 # Stores the y-coordinate of the top pipe.
        self.bottom = 0 #Stores the y-coordinate of the bottom pipe.
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True) #Stores the flipped version of the pipe image (for the top pipe).(False => flip horizontally, True => flip vertically)
        self.PIPE_BOTTOM = PIPE_IMAGE #Stores the bottom pipe image.

        self.passed = False #Stores whether the bird has passed the pipes or not.(used for collisions and neat score)
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450) #Randomly generate the height of the pipes between 50 and 450
        '''
        Since the top pipe is inverted and the bottom of the top pipe is to be shown,
        we have the self.height where the pipe as to be placed and the height of the pipe self.PIPE_TOP.get_height()
        But if the top of the pipe is placed at self.height, the bottom of the pipe will be at self.height + self.PIPE_TOP.get_height(), which is incorrect,
        hence we subtract the self.PIPE_TOP.get_height() from self.height to get the correct position of the top of the pipe. 
        '''
        self.top = self.height - self.PIPE_TOP.get_height() 
        self.bottom = self.height + self.GAP #since the measuring starts from the left corner of the window, the bottom pipe is placed after the self.height and the gap between the top pipe and the bottom pipe

    def move(self):
        self.x -= self.VEL #Move the pipes towards the bird by decreasing the x-coordinate of the pipes by the value of the velocity.(pixels per game frame)

    def draw(self, window):
        window.blit(self.PIPE_TOP,(self.x, self.top)) #Draw the top pipe on the window at the x and top position
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom)) #Draw the bottom pipe on the window at the x and bottom position

    def collide(self, bird):
        '''
        Using masks to check for collisions between the bird and the pipes.
        Masks are used to check for pixel perfect collisions.
        Or else rectangles are used to check for collisions which can lead to false positives.
        A mask is a 2D array where each pixel is either 1 (opaque) or 0 (transparent). (bit mask or binary representation)
        It helps with pixel-perfect collision detection by checking exact pixels instead of using simple rectangles.
        '''
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        '''
        Offset tells us how much the pipe's mask needs to be shifted 
        to align with the bird's mask before checking for overlapping pixels.
        Eg: If the bird is at (100, 200) and the pipe is at (250, 300),
        the offset would be (150, 100). This means the pipe is 150 pixels
        to the right and 100 pixels down compared to the bird.
        '''
        top_offset = (self.x - bird.x, self.top - round(bird.y)) #To check for collision we use mask.overlap() which takes only integer values,
        #bird.y may be decimal due to the gravity and jump calculations. Hence we round it.

        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_collide_point = bird_mask.overlap(bottom_mask, bottom_offset) #If no collision then output is none
        top_collide_point = bird_mask.overlap(top_mask, top_offset)

        return bottom_collide_point or top_collide_point
    
class Base:
    VEL = 5
    WIDTH = BASE_IMAGE.get_width()
    IMG = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        '''
        We use 2 base images to create an illusion of an endless scrolling background.
        The image (x1) starts at position 0, and x2 starts right next to it at self.WIDTH.
        Both x1 and x2 move left (-= self.VEL).
        When x1 + self.WIDTH < 0, it means the first image (x1) has completely moved out of the screen from the left and the x2 is at position 0.
        Instead of deleting or resetting x1, we move it to the right of x2 using self.x1 = self.x2 + self.WIDTH (same thing happens when x2 is competely out of the screen),
        effectively cycling it back for an infinite scrolling effect.
        This ensures that as one image moves out, another seamlessly replaces it, creating the illusion of an endless scrolling background
        '''

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0 :
            self.x1 = self.x2 + self.WIDTH

        if self.x2 +self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))


def draw_window(window, birds, pipes, base, score):
    window.blit(BG_IMAGE, (0,0))
    text = STAT_FONT.render("Score: "+str(score), 1, (255,255,255))
    
    for pipe in pipes:
        pipe.draw(window)
    window.blit(text, (WIN_WIDTH-10-text.get_width(), 10))
    base.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()

# genomes are the neural networks for each of the bird object. (Each bird has a neural network of its own)
def eval_genomes(genomes, config): 
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    birds = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(650)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False
                pygame.quit()
                quit()
        
        add_pipe = False
        rem = []
        base.move()

        for pipe in pipes:

            pipe.move()

            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x >  pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5:
                bird.jump()
            
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness +=1
            pipes.append(Pipe(600))

        for pipe in rem:
            pipes.remove(pipe)
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() +12 >= (WIN_HEIGHT - (base.IMG.get_height()//2)) or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
            
        
        draw_window(window, birds, pipes, base, score)


def run(config_path):
    #don't need to pass [NEAT] (from the config file) explicitly because neat.config.Config(...) will automatically read it when config_path is provided.
    # pass the 4 components (Genome, Reproduction, SpeciesSet, Stagnation)
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create the population using the config object
    p = neat.Population(config) # use population class

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes,50) # 50 generations


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__) #Get the directory name
    config_path = os.path.join(local_dir, "config.txt") #Get the config path
    run(config_path)