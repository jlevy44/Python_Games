import pygame

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)

# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600




class Player(pygame.sprite.Sprite):
    """Bar that player controls"""
    g = 3

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.t = 0
        self.image = pygame.Surface([15,15])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        """Change speed player"""
        #self.t += 1
        self.change_x += x
        self.change_y += y

        #if not pygame.sprite.spritecollide(self,self.walls,False):
        #    self.change_y += y + self.g
        #else:
        #    self.change_y += y

    def update(self):
        """Update position"""
        #self.calc_grav()
        # move left or right
        self.rect.x += self.change_x

        # did we hit wall
        block_hit_list = pygame.sprite.spritecollide(self,self.walls,False)
        for block in block_hit_list:
            # if move right, set right to left side of hit object
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # move up down
        self.rect.y += self.change_y

        # check and see if hit anything
        block_hit_list = pygame.sprite.spritecollide(self,self.walls,False)
        for block in block_hit_list:
            # if move right, set right to left side of hit object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                #self.change_y = 0
            else:
                self.rect.top = block.rect.bottom
                #self.change_y = 0

class Wall(pygame.sprite.Sprite):
    """Wall player can run into"""
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        # make blue wall with size specified
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        # make top-left corner the passed in
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# initialize game
pygame.init()

# create 800x600 screen
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

# set title window
pygame.display.set_caption('Test')

# List to hold all sprites
all_sprite_list = pygame.sprite.Group()

# make walls
wall_list = pygame.sprite.Group()

wall = Wall(0,0,10,600), Wall(10,0,790,10), Wall(10,0,790,10),Wall(10, 200, 100, 10)
wall_list.add(wall)
all_sprite_list.add(wall)


# create player paddle object
player = Player(50,50)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False
while not done:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:# and pygame.sprite.spritecollide(player,player.walls,False):
                #player.changespeed(0, -3)
                player.changespeed(0,-3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:# and pygame.sprite.spritecollide(player,player.walls,False):
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

        #player.changespeed(0,player.g)


    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()


