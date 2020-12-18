import pygame
import sys
import random
import pickle


######Game Functions ###########
#******* Floor Functions *********
def floor_movement():
    screen.blit(floor_surface,(floor_x_pos, 500))
    screen.blit(floor_surface,(floor_x_pos + 385 ,500))

# ******* Pipe function *****************************
def create_pipe():
    random_pip = random.choice(pipe_height)
       
    bottom_pip = pipe_surface.get_rect(midbottom = (500,random_pip - 150 ))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pip))
    return top_pipe,bottom_pip
    
def pipe_movement(pipes):
    for pipe in pipes:
        pipe.centerx -= 2 
    return pipes

def pipe_draw(pipes):
    for pipe in pipes:
        if pipe.bottom  >= 500:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pip = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pip,pipe)

Spawnpipe = pygame.USEREVENT
pygame.time.set_timer(Spawnpipe,1200)







#************Bird functions ****************

def check_col(pipes):
    global bird_movement
    for pipe in pipes:
        if bird_rect.colliderect(pipe) == True:
            hit_sound.play()
            return False
    if bird_rect.bottom >= 500:
        hit_sound.play()
        return False
    return True


def bird_rotate(bird):
    new_bird =  pygame.transform.rotozoom(bird,bird_movement * -3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (80,bird_rect.centery))
    return new_bird ,new_bird_rect

    

Birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(Birdflap,200)

#****************** Game Score *********************
def score_display(game_state):
    if game_state == 'main_state':
        score_surface = game_font.render(str(int(score)),False,(255,255,255))
        score_rect = score_surface.get_rect(center=(180,40))
        screen.blit(score_surface,score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'score {int(score)}',False,(255,255,255))
        score_rect = score_surface.get_rect(center=(180,40))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High score {int(high_score)}',False,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(180,480))
        screen.blit(high_score_surface,high_score_rect)





def score_check(pipes):
    global score
    for pipe in pipes:
        if pipe.centerx == 60:
            score += 0.5
            score_sound.play( )

def high_score_check(score):
    try:
        with open('highscore.txt','rb') as file:
            high_score = pickle.load(file)
            if score > high_score:
                with open('highscore.txt', 'wb') as file:
                    pickle.dump(score, file)
    except :
        high_score = score
        with open('highscore.txt', 'wb') as file:
            pickle.dump(score, file)
    
    return high_score

#************ Game Reset *****************


## Game lancher
pygame.mixer.pre_init(channels=1)
pygame.init()

#########Game Screen #################
pixels = (360,600)
screen = pygame.display.set_mode(pixels)
icone = pygame.image.load('flappy.ico')
icone = pygame.display.set_icon(icone)
title = pygame.display.set_caption('Flappy Bird')




# *** Clock for the frames of the screen ********
clock = pygame.time.Clock()

#Uplaoding the background image
bg_choice = random.choice(['assets/background-night.png','assets/background-day.png'])
bg_suface  = pygame.image.load(bg_choice).convert()
bg_suface = pygame.transform.scale(bg_suface,pixels)
                                      
#Uploading the floor of the game 
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface= pygame.transform.scale2x(floor_surface)
floor_x_pos = 0



#Uploading the player of the game ('It's a bird')
bc = random.choice(['bluebird-','redbird-','yellowbird-'])
bird_midflap = pygame.image.load('assets/'+bc+'midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/'+bc+'upflap.png').convert_alpha()
bird_downflap = pygame.image.load('assets/'+bc+'downflap.png').convert_alpha()
bird_frames = [bird_upflap,bird_midflap,bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (80,300))




#Uploading pipes 
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()

# Game Over 
gameover_surface = pygame.image.load('assets/message.png').convert_alpha()
gameover_surface = pygame.transform.scale(gameover_surface,(200,350))
gameover_rect = gameover_surface.get_rect(center=(180,250))

####Game Variables ############
gravity = 0.25
bird_movement = 0
pipe_list = []
pipe_height = [180,250,300,350,400]
game_active = True
score = 0
high_score = 0
space = 0
game_font = pygame.font.Font('04B_19.ttf',30)

#***********Sounds ***********************
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav') 

#######Game loop #######
while True:
#Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7  
                flap_sound.play()
                    
            if event.key == pygame.K_SPACE and not game_active:
                score = 0
                bird_movement = -3
                bird_rect.center = (80,300)
                pipe_list = []
                game_active = True
                
        
        
        if event.type == Spawnpipe:
            pipe_list.extend(create_pipe()) 
        
        if event.type == Birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface,bird_rect = bird_animation()  
                    
#Screen Background    
    screen.blit(bg_suface,(0,0))

    
    if game_active:
    #Bird
        bird_movement += gravity
        bird_rot = bird_rotate(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(bird_rot,bird_rect)
        
    #pipes 
        pipe_list = pipe_movement(pipe_list)
        pipe_draw(pipe_list)
        score_check(pipe_list)
        score_display('main_state')
        high_score = high_score_check(score)
        game_active = check_col(pipe_list)
    else:
        score_display('game_over')
        screen.blit(gameover_surface,gameover_rect)
        
        
#Floor
    floor_movement()
    floor_x_pos -=1
    if floor_x_pos < -385:
        floor_x_pos = 0


#updating the screen 
    pygame.display.update()
    # In the clock here im chosing how many frame limit should i have for the screen wich is 120 fps in my case
    clock.tick(100)
    
    