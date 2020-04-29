import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600
backgroundImg = pygame.image.load('grass.jpg')
backgroundImg = pygame.transform.scale(backgroundImg, (display_width, display_height))

# pause_music = pygame.mixer.music.load('aguadebeber.wav')
crash_sound = pygame.mixer.Sound("crash.wav")

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

rabbit_width = 73
# sets up game display to specified width/height
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dodger Rabbit')
clock = pygame.time.Clock()

pause = False


rabbitImg = pygame.image.load('rabbit.png')
rabbitImg = pygame.transform.scale(rabbitImg, (100, 100))

foxImg = pygame.image.load('fox.png')
foxImg = pygame.transform.scale(foxImg, (100,100))

carrotImg = pygame.image.load('carrot.png')
carrotImg = pygame.transform.scale(carrotImg, (100,100))



# text displaying function showing items dodged
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Foxes Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def carrots_munched(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Carrots Munched: "+str(count), True, black)
    gameDisplay.blit(text,(150,0))


def fox(x,y,w,h):
    gameDisplay.blit(foxImg,(x,y,w,h))

def carrot(x,y,w,h):
    gameDisplay.blit(carrotImg,(x,y,w,h))
    

def rabbit(x,y):
    gameDisplay.blit(rabbitImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.SysFont("comicsansms", 1)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()
    
    

def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    message_display('You crashed!')

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause 
    pause = False
    pygame.mixer.music.unpause()
    pygame.mixer.music.load('londonCalling.wav')
    pygame.mixer.music.play(-1)

    



# button function takes in a message, placement, active color, inactive color, and default no action
def button(message,x,y,w,h,inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # only want to know if clicked within bounds of button
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color,(x,y,w,h))
        if click[0] == 1 and action != None:
            # will run action defined in parameters on click
            action()         
    else:
        # otherwise stays inactive
        pygame.draw.rect(gameDisplay, inactive_color,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def paused():
    # pause music
    pygame.mixer.music.pause()
    pygame.mixer.music.load('aguadebeber.wav')
    pygame.mixer.music.play(-1)

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    # while pause = true 
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                
        #gameDisplay.fill(white)
        

        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)  
    
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                quitgame()
        
        
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",100)
        TextSurf, TextRect = text_objects("Dodger Rabbit", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Hop ( :",150,450,100,50,green,bright_green, game_loop)
        button("Quit ) :",550,450,100,50,red,bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


    
def game_loop():
    pygame.mixer.music.load('londonCalling.wav')
    pygame.mixer.music.play(-1)

    global pause 

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    # left or right directional change for rabbit 
    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    carrot_startx = random.randrange(0, display_width)
    carrot_speed = 4
    carrot_starty = -600
    carrot_width = 100 
    carrot_height = 100

    dodged = 0
    munched = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                # when p is pressed pause is equal to true and pause function runs
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        gameDisplay.fill(white)
        gameDisplay.blit(backgroundImg,(0,0)) 
        # begins the carrot and the fox falling 
        thing_starty += thing_speed
        carrot_starty += carrot_speed

        rabbit(x,y)
        fox(thing_startx, thing_starty,thing_width, thing_height)
        carrot(carrot_startx, carrot_starty,carrot_width, carrot_height)


        things_dodged(dodged)
        carrots_munched(munched)

        # crash if rabbit goes off left or right screen
        if x > display_width - rabbit_width or x < 0:
            crash()
        # when a block re-generates, add 1 to dodged 
        # increase thing speed 
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1

        if y < thing_starty+thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x+rabbit_width > thing_startx and x + rabbit_width < thing_startx+thing_width:    
                crash()

        if carrot_starty > display_height: 
            carrot_starty = 0 - carrot_height
            carrot_startx = random.randrange(0,display_width)
            

        if y < carrot_starty+carrot_height:
            if x > carrot_startx and x < carrot_startx + carrot_width or x+rabbit_width > carrot_startx and x + rabbit_width < carrot_startx + carrot_width:     
                munched += 1
                
                
               
        
        pygame.display.update()
        clock.tick(60)
game_intro()
game_loop()
pygame.quit()
quit()