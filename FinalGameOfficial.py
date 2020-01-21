"""
Get Fish:

The purpose of the game is to pass all 6 levels. In each level, you must collect all the fish and water within the time limit. You are starting off with 3 lives. If you collect a puffle, you will gain an extra life. Lives allow you to continue to play after being eaten by a shark or killed by an iceberg.If you don't complete the level in the allotted time, the game is over. If you die with no lives, you must start the entire game over. Good luck.

"""
# Imports 
import pygame
import random

# Initialize Pygame
pygame.init()

# Sounds

shark_sound = pygame.mixer.Sound("shark.wav")

puffle_sound = pygame.mixer.Sound("puffle.wav")

fish_sound = pygame.mixer.Sound("fish.wav")

bump_sound = pygame.mixer.Sound("bump.wav")

background_sound = pygame.mixer.Sound("background.wav")

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (66, 134, 244) 
GREEN = (66, 244, 80)

# Fonts
game_font = pygame.font.SysFont('Calibri', 100, True, False)
my_font = pygame.font.SysFont('Calibri', 40, True, False)
intro_font = pygame.font.SysFont('Courier', 30, True, False)
 
# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Set global Variables with screen 
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Starting Code for cut screen class
def cut_screen(color, message):
    '''
    Place this function BEFORE the main game loop.  
    Alter it as needed for your game.
    It has its own game loop (different from the main loop)
    When you run this function, it will continue looping with the message provided until you press a key
    If you have instructions or special animations, you might want to make two different functions for intro and game_over screens to be called separately
    '''
    done = False # loop condition to end the function
    intro_font = pygame.font.SysFont('Courier', 30, True, False)
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                done = True # this ends the intro loop
                print(event.key)
               
        screen.fill(color)
        my_text = intro_font.render(message, True, BLACK)
        
        # these two lines will center up your text if you want that
        center_x = (SCREEN_WIDTH // 2) - (my_text.get_width() // 2)
        center_y = (SCREEN_HEIGHT // 2) - (my_text.get_height() // 2)  
        screen.blit(my_text, [center_x, center_y])
        
        pygame.display.flip()
        clock.tick(60)    

# Player Class
class Player(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
        self.image = pygame.Surface([10,15])
 
        # Set height, width
        self.img = pygame.image.load("player.png")
       
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x + 20
        self.rect.y = y + 20
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            bump_sound.play()
        if self.rect.x < 0:
            self.rect.x = 0 
            bump_sound.play()
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            bump_sound.play()
        if self.rect.y < 0:
            self.rect.y = 0
            bump_sound.play()
    
    def draw_me(self):
        screen.blit(self.img, (self.rect.x - 20, self.rect.y - 20))
            
# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super().__init__()
        
        self.image = pygame.image.load(image_name) # use variable 
        
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()  
       
        self.kind = "Shark"

# Life Class
class Life(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super().__init__()
        
        self.image = pygame.image.load(image_name)
        
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()   
        
        self.kind = "Puffle"

# PowerUp Class
class Power(pygame.sprite.Sprite):
    def __init__(self, image_name):
        super().__init__()
        
        self.image = pygame.image.load(image_name)
        
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()   
        
        self.kind = "Fish"

# Set caption for screen 
pygame.display.set_caption("Get Fish")

# Create Sprites list
game_list = pygame.sprite.Group()

# This is a list of 'sprites.' Each object in the program is
# added to this list. The list is managed by a class called 'Group.'
all_sprites_list = pygame.sprite.Group()
good_sprites_list = pygame.sprite.Group()
bad_sprites_list = pygame.sprite.Group()

# Create Player 
player = Player(0, 0)
all_sprites_list.add(player)

# Other sprites list for good and bad sprites
for i in range(7):
    # This represents a fish
    fish = Power("fish.png")
    collided = True
    while collided:
        collided = False
        # Set a random location for the fish
        fish.rect.x = random.randrange(SCREEN_WIDTH - fish.rect.width)
        fish.rect.y = random.randrange(SCREEN_HEIGHT - fish.rect.height)
        hit_list = pygame.sprite.spritecollide(fish, all_sprites_list, False)
        for hit in hit_list:
            collided = True
            
    # Add the fish to the list of objects
    good_sprites_list.add(fish)
    all_sprites_list.add(fish)
    
for i in range(2):
    # This represents a puffle
    puffle = Life("puffle.png")
    collided = True
    while collided:
        collided = False
        # Set a random location for the puffle
        puffle.rect.x = random.randrange(SCREEN_WIDTH - puffle.rect.width)
        puffle.rect.y = random.randrange(SCREEN_HEIGHT - puffle.rect.height)
        hit_list = pygame.sprite.spritecollide(puffle, all_sprites_list, False)
        for hit in hit_list:
            collided = True
        
    # Add the puffle to the list of objects
    good_sprites_list.add(puffle)
    all_sprites_list.add(puffle)    

for i in range(7):
    # This represents water
    water = Power("water.png")
    collided = True
    while collided:
        collided = False
        # Set a random location for the water
        water.rect.x = random.randrange(SCREEN_WIDTH - water.rect.width)
        water.rect.y = random.randrange(SCREEN_HEIGHT - water.rect.height)
        hit_list = pygame.sprite.spritecollide(water, all_sprites_list, False)
        for hit in hit_list:
            collided = True     
            
    # Add the water to the list of objects
    good_sprites_list.add(water)
    all_sprites_list.add(water)

for i in range(10):
    # This represents a shark 
    shark = Enemy("shark.png")
    collided = True
    while collided:
        collided = False
        # Set a random location for the shark
        shark.rect.x = random.randrange(SCREEN_WIDTH - shark.rect.width)
        shark.rect.y = random.randrange(SCREEN_HEIGHT - shark.rect.height)
        hit_list = pygame.sprite.spritecollide(shark, all_sprites_list, False)
        for hit in hit_list:
            collided = True     
            
    # Add the shark to the list of objects
    bad_sprites_list.add(shark)
    all_sprites_list.add(shark)
    
    while shark.rect.x <= player.rect.width and shark.rect.y < player.rect.height:
        shark.rect.x = random.randrange(SCREEN_WIDTH - shark.rect.width)
        shark.rect.y = random.randrange(SCREEN_HEIGHT - shark.rect.height)       
        
for i in range(10):
    # This represents a iceberg  
    ice = Enemy("iceberg.png")
    collided = True
    while collided:
        collided = False
        # Set a random location for the iceberg
        ice.rect.x = random.randrange(SCREEN_WIDTH - ice.rect.width)
        ice.rect.y = random.randrange(SCREEN_HEIGHT - ice.rect.height)
        hit_list = pygame.sprite.spritecollide(ice, all_sprites_list, False)
        for hit in hit_list:
            collided = True
        
    # Add the iceberg to the list of objects
    bad_sprites_list.add(ice)
    all_sprites_list.add(ice)
    
    while ice.rect.x <= player.rect.width and ice.rect.y < player.rect.height:
        ice.rect.x = random.randrange(SCREEN_WIDTH - ice.rect.width)
        ice.rect.y = random.randrange(SCREEN_HEIGHT - ice.rect.height)
        

# Loop until the user clicks the close button.
done = False

# Set up global variable for score 
score = 0 

# Set time for countdown 
time = 46 # variable for countdown timer.  

# Set Level
level = 1 

# Set Lives
lives = 3

# Background Image
background_image = pygame.image.load("background.png")

# Set up start of game
cut_screen(BLUE, "Press any key to start. Good luck.") # this is the call to the function to make intro screen appear

# Set up time lapse 
game_over_countdown = 500

# Play background sound 
background_sound.play()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-4, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(4, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -4)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 4)
         
        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(4, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-4, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 4)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -4)        
    
    # set countdown
    time -= 1/30      
    
    # Create levels   
    if len(good_sprites_list) == 0:
        time = 46
        time -= 1/30
        level += 1
        all_sprites_list.empty()
        good_sprites_list.empty()
        bad_sprites_list.empty()
        all_sprites_list.add(player) 
        bad_sprites = level * 2 + 5 
        good_sprites = level * 2 + 8
        for i in range(good_sprites):
            # This represents a fish
            fish = Power("fish.png")
            collided = True
            while collided:
                collided = False
                # Set a random location for the fish
                fish.rect.x = random.randrange(SCREEN_WIDTH - fish.rect.width)
                fish.rect.y = random.randrange(SCREEN_HEIGHT - fish.rect.height)
                hit_list = pygame.sprite.spritecollide(fish, all_sprites_list, False)
                for hit in hit_list:
                    collided = True
                    
            # Add the fish to the list of objects
            good_sprites_list.add(fish)
            all_sprites_list.add(fish)
            
        for i in range(2):
            # This represents a puffle
            puffle = Life("puffle.png")
            collided = True
            while collided:
                collided = False
                # Set a random location for the puffle
                puffle.rect.x = random.randrange(SCREEN_WIDTH - puffle.rect.width)
                puffle.rect.y = random.randrange(SCREEN_HEIGHT - puffle.rect.height)
                hit_list = pygame.sprite.spritecollide(puffle, all_sprites_list, False)
                for hit in hit_list:
                    collided = True
                
            # Add the puffle to the list of objects
            good_sprites_list.add(puffle)
            all_sprites_list.add(puffle)    
        
        for i in range(good_sprites):
            # This represents water
            water = Power("water.png")
            collided = True
            while collided:
                collided = False
                # Set a random location for the water
                water.rect.x = random.randrange(SCREEN_WIDTH - water.rect.width)
                water.rect.y = random.randrange(SCREEN_HEIGHT - water.rect.height)
                hit_list = pygame.sprite.spritecollide(water, all_sprites_list, False)
                for hit in hit_list:
                    collided = True     
                    
            # Add the water to the list of objects
            good_sprites_list.add(water)
            all_sprites_list.add(water)
        
        for i in range(bad_sprites):
            # This represents a shark 
            shark = Enemy("shark.png")
            collided = True
            while collided:
                collided = False
                # Set a random location for the shark
                shark.rect.x = random.randrange(SCREEN_WIDTH - shark.rect.width)
                shark.rect.y = random.randrange(SCREEN_HEIGHT - shark.rect.height)
                hit_list = pygame.sprite.spritecollide(shark, all_sprites_list, False)
                for hit in hit_list:
                    collided = True     
                    
            # Add the shark to the list of objects
            bad_sprites_list.add(shark)
            all_sprites_list.add(shark)
            
            while shark.rect.x <= player.rect.width and shark.rect.y < player.rect.height:
                shark.rect.x = random.randrange(SCREEN_WIDTH - shark.rect.width)
                shark.rect.y = random.randrange(SCREEN_HEIGHT - shark.rect.height)       
                
        for i in range(bad_sprites):
            # This represents a iceberg  
            ice = Enemy("iceberg.png")
            collided = True
            while collided:
                collided = False
                # Set a random location for the iceberg
                ice.rect.x = random.randrange(SCREEN_WIDTH - ice.rect.width)
                ice.rect.y = random.randrange(SCREEN_HEIGHT - ice.rect.height)
                hit_list = pygame.sprite.spritecollide(ice, all_sprites_list, False)
                for hit in hit_list:
                    collided = True
                
            # Add the iceberg to the list of objects
            bad_sprites_list.add(ice)
            all_sprites_list.add(ice)
            
            while ice.rect.x <= player.rect.width and ice.rect.y < player.rect.height:
                ice.rect.x = random.randrange(SCREEN_WIDTH - ice.rect.width)
                ice.rect.y = random.randrange(SCREEN_HEIGHT - ice.rect.height)
                
    # Blit background image 
    screen.blit(background_image, [0, 0]) 
    
    # See if the player block has collided with anything.
    hit_list = pygame.sprite.spritecollide(player, good_sprites_list, True)
    hit_list2 = pygame.sprite.spritecollide(player, bad_sprites_list, True) 
    
    # Make collisions 
    for hit in hit_list:
        if hit.kind == "Puffle":
            lives += 1
            puffle_sound.play()
        if hit.kind == "Fish":
            fish_sound.play()
      
    # Make collisions       
    for hit in hit_list2:
        if hit.kind == "Shark":
            lives -= 1
            shark_sound.play()
        player.rect.x = 20
        player.rect.y = 20 
     
    # End when time runs out 
    if time <= 0:
        done = False # loop condition to end the function
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    done = True # this ends the intro loop
                    print(event.key)
            game_over_countdown -= 1
            # Make screen red 
            screen.fill(RED)
            # set varables for text
            center_x = (SCREEN_WIDTH // 2) - (my_text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (my_text.get_height() // 2)         
            # Create Text
            my_text = intro_font.render("Time ran out.", True, WHITE)       
            my_text2 = intro_font.render("Game over.", True, WHITE)       
            my_text3 = intro_font.render("Press any key to quit.", True, WHITE)       
            # Blit text 
            screen.blit(my_text,[center_x, center_y - 30]) 
            screen.blit(my_text2,[center_x, center_y]) 
            screen.blit(my_text3,[center_x, center_y + 30]) 
            # End game 
            if game_over_countdown < 0:
                done = True
            # Flip the screen
            pygame.display.flip()
                
            # Set window time 
            clock.tick(60)                    
  
    # If you have no lives, must die   
    if lives <= 0:
        done = False # loop condition to end the function
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    done = True # this ends the intro loop
                    print(event.key)
            game_over_countdown -= 1
            # Make screen red 
            screen.fill(RED)
            # set varables for text
            center_x = (SCREEN_WIDTH // 2) - (my_text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (my_text.get_height() // 2)         
            # Create Text
            my_text = intro_font.render("You died with no lives left.", True, WHITE)       
            my_text2 = intro_font.render("Game over.", True, WHITE)       
            my_text3 = intro_font.render("Press any key to quit.", True, WHITE)       
            # Blit text 
            screen.blit(my_text,[center_x, center_y - 30]) 
            screen.blit(my_text2,[center_x, center_y]) 
            screen.blit(my_text3,[center_x, center_y + 30]) 
            # End game 
            if game_over_countdown < 0:
                done = True
            # Flip the screen
            pygame.display.flip()
                
            # Set window time 
            clock.tick(60)                    
           
    
    # Make a cap at how many levels are in the game. Also end the game
    while level > 6 and game_over_countdown > 0:
        done = False # loop condition to end the function
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    done = True # this ends the intro loop
                    print(event.key)        
            game_over_countdown -= 1
            screen.fill(RED)
            center_x = (SCREEN_WIDTH // 2) - (my_text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (my_text.get_height() // 2)         
            my_text = intro_font.render("You beat all the levels. You won!. Game over.", True, WHITE)        
            screen.blit(my_text,[center_x, center_y])
            if game_over_countdown < 0:
                done = True
            # Flip the screen
            pygame.display.flip()
            
            # Set window time 
            clock.tick(60)        
    
   
    # Draw all the spites
    all_sprites_list.update()
    all_sprites_list.draw(screen) 
    player.draw_me()
   
    # Score on screen   
    my_text = my_font.render("Level: " + str(level), True, RED)
    screen.blit(my_text,[25, 25]) 
    my_text2 = my_font.render("Time: " + str(int(time)), True, RED)
    screen.blit(my_text2, [25, 50])
    my_text3 = my_font.render("Lives: " + str(lives), True, RED)
    screen.blit(my_text3, [25, 75]) 
                      
    # Flip the screen
    pygame.display.flip()
    
    # Set window time 
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()

