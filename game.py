#Space battle

import pygame as pg
import random as rd


pg.init()

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

enemy = pg.image.load('img\enemy1.png').convert_alpha()
enemy = pg.transform.scale(enemy,(50,50))


power = pg.image.load('img\power.png')
power = pg.transform.scale(power,(50,50))



position_power_x = 100
position_power_y = 425

position_player_x = 100
position_player_y = 400

position_enemy_x = 500
position_enemy_y = 350


# ---------------------------------------------------------------------------
#game running


speed_x_power = 0
position_x_power = 300
position_y_power = 300



running = True
points = 5
trigged = False
score_font = pg.font.SysFont('LeagueSpartan-Medium.ttf',60)


player_ret = player.get_rect()
power_ret = power.get_rect()
enemy_ret = enemy.get_rect()



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

def colisions():
    global points
    if player_ret.colliderect(enemy_ret) or enemy_ret.x == 50:
        points -= 5
        return True
    elif power_ret.colliderect(enemy_ret):
        points += 2
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
    if Key_board[pg.K_UP] and position_player_y > 1:
        position_player_y -=1
        if not trigged:
            position_power_y -=1
        
    if Key_board[pg.K_DOWN] and position_player_y < 600:
        position_player_y +=1
        if not trigged:
            position_power_y +=1
        
    
    if Key_board[pg.K_SPACE]:
        trigged = True
        speed_x_power = 2
        
    if points < 0:
        running = False    
    
    
    #respawn enemy
    if position_enemy_x == 20:
        position_enemy_x = respawn()[0]
        position_enemy_y = respawn()[1]
        
    #reload power
    if position_power_x == 1280:
        position_power_x,position_power_y,trigged,speed_x_power = reload_power()
        
    #repawn enemy
    if position_enemy_x == 20 or colisions():
        position_enemy_x = respawn()[0]
        position_enemy_y = respawn()[1]
    
    #position ret
    
    player_ret.y = position_player_y
    player_ret.x = position_player_x
    
    power_ret.y = position_power_y
    power_ret.x = position_power_x
    
    
    enemy_ret.x = position_enemy_x
    enemy_ret.y = position_enemy_y
    
    
    #move
    x-=0.5
    position_enemy_x -=1
    position_power_x += speed_x_power
    

    
    # pg.draw.rect(screen,(255,0,0),player_ret,4)
    # pg.draw.rect(screen,(255,0,0),power_ret,4)
    # pg.draw.rect(screen,(255,0,0),enemy_ret,4)
    
    score = score_font.render(f'Score: {int(points)}',True,(255,255,255))
    screen.blit(score,(50,50))
    

    #ploting images
    screen.blit(power,(position_power_x,position_power_y))
    screen.blit(player, (position_player_x,position_player_y))
    screen.blit(enemy, (position_enemy_x,position_enemy_y))
    
    # print(points) para conferir no terminal se esta funcionando
    pg.display.update()
