#Space battle

import pygame as pg
import random as rd


pg.init()
pg.joystick.init()
# joystick = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
joystick = pg.joystick.Joystick(0)



# ---------------------------------------------------------------------------
#screen size

x = 1280
y = 720

screen = pg.display.set_mode((x,y))

# ---------------------------------------------------------------------------
#window name

pg.display.set_caption('Space Battle')


# ---------------------------------------------------------------------------

bg = pg.image.load('img/bg.jpg').convert_alpha()
bg = pg.transform.scale(bg,(x,y))

player = pg.image.load('img\player.png').convert_alpha()
player = pg.transform.scale(player,(100,100))

enemy1 = pg.image.load('img\enemy1.png').convert_alpha()
enemy1 = pg.transform.scale(enemy1,(50,50))

enemy2 = pg.image.load('img\enemy2.png').convert_alpha()
enemy2 = pg.transform.scale(enemy2,(50,50))


power = pg.image.load('img\power.png')
power = pg.transform.scale(power,(50,50))


position_power_x = 100
position_power_y = 425

position_player_x = 100
position_player_y = 400

position_enemy1_x = 500
position_enemy1_y = 350

position_enemy2_x = 450
position_enemy2_y = 350

points = 28
speed_x_power = 10
position_x_power = 300
position_y_power = 300

running = True

trigged = False
score_font = pg.font.SysFont('LeagueSpartan-Medium.ttf',60)

# ---------------------------------------------------------------------------
#game running

player_ret = player.get_rect()
power_ret = power.get_rect()
enemy1_ret = enemy1.get_rect()
enemy2_ret = enemy2.get_rect()


#repawn enemies
def respawn():
    x = 1350
    y = rd.randint(1,640)
    return [x,y]

def reload_power():
    trigged = False
    reload_power_x = position_player_x 
    reload_power_y = position_player_y + 21
    speed_x_power = 0
    return[reload_power_x,reload_power_y,trigged,speed_x_power]


#score system
def colisions1():
    global points
    if player_ret.colliderect(enemy1_ret) or enemy1_ret.x == 40:
        points -= 2.5
        return True
    elif power_ret.colliderect(enemy1_ret):
        points += 1
        return True
    else:
        return False
    
def colisions2():
    global points
    if player_ret.colliderect(enemy2_ret) or enemy2_ret.x == 40:
        points -= 2.5
        return True
    elif power_ret.colliderect(enemy2_ret):
        points += 1
        return True
    else:
        return False

#game running
while running:
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            running = False
    screen.blit(bg,(0,0))

    
    rel_x = x % bg.get_rect().width
    screen.blit(bg,(rel_x - bg.get_rect().width,0))
    if rel_x < 1280:
        screen.blit(bg,(rel_x,0))
    
    
    #keyboard_controls
    Key_board = pg.key.get_pressed()
    if (Key_board[pg.K_UP] and position_player_y > 1) or (joystick.get_button(3) and position_player_y > 1):
        position_player_y -=1
        if not trigged:
            position_power_y -=1
        

    if (Key_board[pg.K_DOWN] and position_player_y < 600) or (joystick.get_button(0) and position_player_y < 600):
        position_player_y +=1
        if not trigged:
            position_power_y +=1
    
    
    # if event.type == pg.JOYBUTTONDOWN:
    #     print(event)    
    
    if Key_board[pg.K_SPACE] or joystick.get_button(4) or joystick.get_button(5):
        trigged = True
        speed_x_power = 5
        
    if points < 0:
        running = False    
    
    
    #respawn enemy 1
    if position_enemy1_x == 20:
        position_enemy1_x = respawn()[0]
        position_enemy1_y = respawn()[1]
        
        
    #respawn enemy 1  
    if position_enemy2_x == 20:
        position_enemy2_x = respawn()[1]
        position_enemy2_y = respawn()[0]
    
    
    #reload power
    if position_power_x == 1200 or colisions2() or colisions1():
        position_power_x,position_power_y,trigged,speed_x_power = reload_power()
        
    #repawn enemy
    if position_enemy1_x == 20 or colisions1():
        position_enemy1_x = respawn()[0]
        position_enemy1_y = respawn()[1]
     #repawn enemy 2
    if position_enemy2_x == 20 or colisions2():
        position_enemy2_x = respawn()[0]
        position_enemy2_y = respawn()[1]
        
    
    #position ret
    
    player_ret.y = position_player_y
    player_ret.x = position_player_x
    
    power_ret.y = position_power_y
    power_ret.x = position_power_x
    
    
    enemy1_ret.x = position_enemy1_x
    enemy1_ret.y = position_enemy1_y
    
    enemy2_ret.x = position_enemy2_x
    enemy2_ret.y = position_enemy2_y
    

    #move
    x-= 5
    position_enemy1_x -=1
    position_enemy2_x -=1
    position_power_x += speed_x_power
    

    # pg.draw.rect(screen,(255,0,0),player_ret,4)
    # pg.draw.rect(screen,(255,0,0),power_ret,4)
    # pg.draw.rect(screen,(255,0,0),enemy_ret,4)
    
    score = score_font.render(f'Score: {int(points)}',True,(255,255,255))
    screen.blit(score,(50,50))
    

    #ploting images
    screen.blit(power,(position_power_x,position_power_y))
    screen.blit(player, (position_player_x,position_player_y))
    screen.blit(enemy1, (position_enemy1_x,position_enemy1_y))
    screen.blit(enemy2, (position_enemy2_x,position_enemy2_y))
    
    # print(points) para conferir no terminal se esta funcionando
    # pg.display.update()
    pg.display.flip()
