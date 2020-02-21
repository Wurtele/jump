import time, random, pygame, sys
"""
Name: Jump
By Owen Wurtele


This program is a game called Jump.
To start press space.
To pause press R
To quit press X
You will then control an orange slime character.
Your goal is to collect as many of the coins as possible.
If you are touched by the green slime blocks it is gameover.
In the gameover screen press space to play again
"""

###CLASSES###
"""Class for player sprite and enemy sprites"""
class Mob(pygame.sprite.Sprite):
    """
    initializes sprite
    defines variables for the sprite
    """
    def __init__(self,type,platform_list, x, y):
        super().__init__()
        self.type = type #type -> if mob is enemy or player
        
        if type == 'player':
            self.image = player_move
        elif type == 'enemy':
            self.image = enemy_img
            self.towards_player = 0
            
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()


        
        self.rect.x = x * 32
        self.rect.y = y * 32
        self.change_x = 0
        self.change_y = 0
        self.platform_list = platform_list

    """
    update performed every loop to move the mob
    """
    def update(self):
        # Gravity
        self.calc_grav()

        if self.type == 'player': #If type is a player move using player input
            self.change_x1,self.change_x2 = 0,0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]: #if w or up down jump up
                self.jump('up')
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: #if s or down down jump down
                self.jump('down')
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: #if a or left down move left
                self.change_x1 = -6
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: #if d or right down move right
                self.change_x2 = 6 
            self.change_x = self.change_x1 + self.change_x2 #self.change_x -> speed of the sprite

        elif self.type == 'enemy': #If type is enemy move using AI
            move_list = [self.towards_player,-0.12,0.12] #possible movements for enemies
            if self.change_x >= 5: #If speed is >=5 decrease speed
                self.change_x += -0.12
            elif self.change_x <= -5: #If speed is <=-5 increase speed
                self.change_x += 0.12
            else: #move enemy based on random choice from move_list
                self.change_x += random.choice(move_list) 

        #changes sprite image to face proper direction
        if self.type == 'player': #if mob type is player
            temp = player_still
            if self.change_x > 0: #if speed is positive player img faces right
                temp = pygame.transform.flip(player_move,True,False)
            elif self.change_x < 0: #if speed is negative player img faces left
                temp = player_move
            if grav == 1: #if grav == 1 -> player img is rightside up
                temp = pygame.transform.flip(temp,False,False)
            else: #if grav == -1 -> player img is upside down
                temp = pygame.transform.flip(temp,False,True)

        elif self.type == 'enemy': #if mob type is enemy
            temp = enemy_img #enemy img defaults to rightside up
            if grav == -1: #if grav == -1 -> flip enemy img upside down
                temp = pygame.transform.flip(enemy_img,False,True)
        self.image = temp #set img to proper orientation
        
        
        # Move left/right
        self.rect.x += self.change_x

        # See if anything got hit
        block_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        for block in block_hit_list:
            # If moving right
            # set  right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if moving left, do the opposite.
                self.rect.left = block.rect.right
            self.change_x = 0

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        for block in block_hit_list:
            #if moving down
            # Reset position to the top of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0: #otherwise if moving up, set top to bottom of object
                self.rect.top = block.rect.bottom

            # stop movement
            self.change_y = 0

    """ Calculate effect of gravity. """
    def calc_grav(self):
        if grav == 1: #if grav is 1
            if self.change_y == 0: #if y speed is 0 set speed to 1
                self.change_y = 1
            else: #if speed is not 0, increase speed down
                self.change_y += .30

            #check if on bottom of screen, if on edge of screen, speed is set to zero
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = SCREEN_HEIGHT - self.rect.height
        elif grav == -1: 
            if self.change_y == 0: #if x speed is 0 set speed to -1
                self.change_y = -1
            else: #if speed is not 0, increase speed upwards
                self.change_y -= .30
            #check if on top of screen, if on top, set speed to 0
            if self.rect.y <= 0 and self.change_y <= 0:
                self.change_y = 0
                self.rect.y = 0

    """Jump up or down"""
    def jump(self,dir):
        if dir == "up": #if jump direction is up
            #move mob down to check if it collides with the ground
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
            self.rect.y -= 2 #reset to previous position

            # If it is ok to jump, set speed up
            if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.change_y = -9
                if self.type == 'player':
                    jump_snd.play()
        else: #if jump direction is down
            #move mob up to check if it collides with the ground
            self.rect.y -= 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
            self.rect.y += 2

            # If it is ok to jump, set speed down
            if len(platform_hit_list) > 0 or self.rect.bottom <= 1:
                self.change_y = 9
                if self.type == 'player':
                    jump_snd.play()

"""Class for platforms that the player and enemy sprites stand on"""
class Platform(pygame.sprite.Sprite):
    """
    initializes sprite
    defines variables for the sprite
    """
    def __init__(self,img, x, y):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x * 32
        self.rect.y = y * 32

"""Class for coins"""
class Coin(pygame.sprite.Sprite):
    """
    initializes sprite
    defines variables for the sprite
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = (x * 32)
        self.rect.y = (y * 32)

"""Class for displaying the score in top left corner"""
class Scoreboard(pygame.sprite.Sprite):
    """
    initializes sprite
    defines variables for the sprite
    """
    def __init__(self):
        super().__init__()
        self.score = 0
    """function to update the score"""
    def update(self):
        msg = '  :'+str(self.score)
        self.image = font2.render(msg, True, (0,0,0))
        self.image.blit(coin_img,(12,1))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 32

#FUNCTIONS
"""function to load data from a file into a series of lists"""
def load_data(file):
    file = open(file,'r')
    map_data = []
    for line in file:
        map_data.append(line)
    file.close()
    return map_data

"""reads the series of lists to place platform, player, enemies and coin spawnpoints in the right spots"""
def create_sprites(map_data):
    active_sprite_list = pygame.sprite.Group() #Create active sprite group
    static_sprite_list = pygame.sprite.Group() #Create static sprite group

    platform_list = pygame.sprite.Group() #Create platform group
    enemy_list = pygame.sprite.Group() #Create enemy group

    coin_spawns = [] #Create list of possible coin spawnpoints
    player = ''
    for row, tiles in enumerate(map_data): #Read map data from list
        for col, tile in enumerate(tiles):
            
            if tile == 'P': #IF P create player sprite
                player = Mob('player',platform_list, col, row)
                active_sprite_list.add(player)

            elif tile == 'E': #IF E create enemy sprite
                enemy = Mob('enemy',platform_list, col, row)
                enemy_list.add(enemy)
                active_sprite_list.add(enemy)

            elif tile == 'S': #IF S add to possible coin spawnpoints
                coin_spawns.append([col,row])

            elif tile == 'C' or tile == 'M' or tile == 'L' or tile == 'R': #If Not default '0'
                if tile == 'C': #IF C use center image
                    img = centerPlat_img
                if tile == 'M': #IF M use middle image
                    img = middlePlat_img
                if tile == 'L': #IF L use left image
                    img = leftPlat_img
                if tile == 'R': #IF R use right image
                    img = rightPlat_img
                platform = Platform(img, col, row)
                platform_list.add(platform)
                static_sprite_list.add(platform)

    return [active_sprite_list, static_sprite_list, platform_list, enemy_list, coin_spawns, player]

"""chooses which direction the gravity will face"""
def grav_choice(grav):
    temp = grav
    grav = random.choice(grav_list)
    if temp != grav: #If gravity has changed play sound effect
        gravSwitch_snd.play()
    return grav

"""chooses where the coin will spawn, then places the coin"""
def coin_choice(coinbool):
    if not coinbool: #If no coins on screen make a new coin
            coin_sp = random.choice(coin_spawns)
            coin = Coin(coin_sp[0],coin_sp[1])
            coin_group.add(coin)
            static_sprite_list.add(coin)
            coinbool = True
    return coinbool

"""chooses which enemies will jump"""
def enemy_jump():
    #mobs randomly jump
    for enemy in enemy_list:
        chance = random.randint(1,100)
        if chance>50:
            if grav<0:
                dir = "down"
            else:
                dir = "up"
            enemy.jump(dir)
"""determines which direction is towards the player"""
def enemy_towardsPlayer():
    #determine direction towards player
    for enemy in enemy_list:
        if enemy.rect.x > player.rect.x:
            enemy.towards_player = -0.12
        else:
            enemy.towards_player = 0.12

"""screen shown when the player dies"""
def game_over():
    death.play()
    msg = font.render("GAME OVER",True,(0,0,0))
    screen.blit(msg,(96,320))
    pygame.display.update()
    clock.tick(1)

"""waits for the player to press space before continuing"""
def wait():
    go = False
    while not go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    go = True
            

#### SET UP ####
pygame.init()

#Load Images

#Player images
player_move = pygame.image.load('orange_img_move.png')
player_still = pygame.image.load('orange_img_still.png')
#Enemy image
enemy_img = pygame.image.load('slimeBlock.png')
enemy_img = pygame.transform.scale(enemy_img, (48,48))
#Item images
coin_img = pygame.image.load('coinGold.png')
coin_img = pygame.transform.scale(coin_img, (32,32))
#Platform images
middlePlat_img = pygame.image.load('grassMid.png')
middlePlat_img = pygame.transform.scale(middlePlat_img, (32,32))
leftPlat_img = pygame.image.load('grassLeft.png')
leftPlat_img = pygame.transform.scale(leftPlat_img, (32,32))
rightPlat_img = pygame.image.load('grassRight.png')
rightPlat_img = pygame.transform.scale(rightPlat_img, (32,32))
centerPlat_img = pygame.image.load('grassCenter.png')
centerPlat_img = pygame.transform.scale(centerPlat_img, (32,32))


#Load Sounds
gravSwitch_snd = pygame.mixer.Sound('gravSwitch.wav')
gravSwitch_snd.set_volume(0.2)
death = pygame.mixer.Sound('death.wav')
death.set_volume(0.2)
jump_snd = pygame.mixer.Sound('jump.wav')
jump_snd.set_volume(0.2)
pickupCoin_snd = pygame.mixer.Sound('Pickup_Coin.wav')
pickupCoin_snd.set_volume(0.2)

#Load Music
pygame.mixer.music.load('airship.mp3')
pygame.mixer.music.set_volume(0.3)

# Set the height and width of the screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen_size = [1024,768]
screen = pygame.display.set_mode(screen_size,pygame.FULLSCREEN|pygame.HWSURFACE)
#Load fonts and set window caption
font=pygame.font.SysFont("monospace",150)
font2 = pygame.font.SysFont("monospace",32)
pygame.display.set_caption("Jump")

#Begin playing music
pygame.mixer.music.play(loops=-1) #Play background music on repeat

#Load mapdata for start screen
map_data = load_data('startScreen.txt') #Reads map data from file
temp = create_sprites(map_data)
static_sprite_list = temp[1]
#Display start screen
screen.fill((173,216,230)) #Clear Screen
static_sprite_list.draw(screen)
pygame.display.flip()
wait()

while True:
    map_data = load_data('map.txt') #Reads map data from file
    temp = create_sprites(map_data)
    active_sprite_list, static_sprite_list, platform_list, enemy_list, coin_spawns, player = temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]

    clock = pygame.time.Clock()
    start = time.time() #Timer started
    pause = 5 #Seconds in between Coin spawning and Gravity inversion
    time.clock() 

    grav = 1 #Default Gravity direction
    grav_list = [1,-1] #Possible Gravity directions

    coin_group = pygame.sprite.GroupSingle() #Coin group for coin
    coin_sp = random.choice(coin_spawns) #Where coin will spawn
    coin = Coin(coin_sp[0],coin_sp[1]) #Creates coin object
    coin_group.add(coin) #Adds coin to coin group
    static_sprite_list.add(coin) #Adds coin to static sprite group
    coinbool = True #Bool for if there is currently a coin on screen

    scoreboard = Scoreboard() #Creates Scoreboard sprite
    active_sprite_list.add(scoreboard) #Adds scoreboard sprite to active sprite group

    done = False #If the game is done (death or quit)
    quit_game = False #If the player has quit
    
    #MAIN LOOP#########################################
    while not done:
        #Every five seconds chance to invert gravity
        elapsed = time.time() - start
        if elapsed >= pause:
            start = time.time()
            grav = grav_choice(grav)
            coinbool = coin_choice(coinbool)
        #Check for player quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    done = True
                    quit_game = True
                if event.key == pygame.K_r:
                    wait()
        #Collisions
        coin_collected = pygame.sprite.spritecollide(player, coin_group, True) #Create list of coins colliding with players
        if coin_collected: #If colliding with any coins increase score 
            scoreboard.score += 1
            coinbool = False
            pickupCoin_snd.play()

        player_caught = pygame.sprite.spritecollide(player, enemy_list, False) #Create list of enemies colliding with players
        if player_caught: #If colliding with any enemies end game
            done = True
        #UPDATE SPRITES
        enemy_jump() #Deternine which enemies will jump
        enemy_towardsPlayer() #Determine which direction is towards the player
        active_sprite_list.update() #Update player and enemies
        #DRAW
        screen.fill((173,216,230)) #Clear Screen
        static_sprite_list.draw(screen) #Draw walls and coins
        active_sprite_list.draw(screen) #Draw player and enemies
        pygame.display.flip() #Update Screen
        clock.tick(60) # Limit to 60 frames per second
    #END OF MAIN LOOP####################################
        

    if not quit_game:
        game_over()
        wait()
    else:
        pygame.quit()
        sys.exit()
