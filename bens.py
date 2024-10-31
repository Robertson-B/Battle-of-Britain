#imported functions
import pgzrun
import random

#defining varibles
WIDTH = 800
HEIGHT = 600

game_state = 0

ship = Actor('plane')
ship.x = 400
ship.y = 450
coin = Actor('yes')
coin.x = random.randint(20, 780)
coin.y = -35
music.play('1942_music')
enemies = []
bullets = []
explodes = []
coinCount = 0
starActivate = False
bullet_delay = 0

score = 0
highscore = 0
wave = 1
wave_timer = 1
hit = 0
bullet = 0
enemy = []
    
lives = 3
game_over = Actor('game over-1')
game_over.y = 400
scroll_speed = 3
scroll1 = Actor('bg', center = (WIDTH/2,HEIGHT/2))
scroll2 = Actor('bg', center = (WIDTH/2,0-HEIGHT/2))
explode = ('explosion')
waves_timer = 1500
enemy_wave = 1
title_screen = Actor('ts')
star = Actor('heart') 
star.x = random.randint(20, 780)
star.y = -35
heartactive = False
heart_timer = 0
heart = 0
hearts = []
game_music = 0


# runs 60 times a second and checks for updates
def update():
    
    #global varibles
    global bullets
    global enemies
    global lives
    global coinCount
    global starActivate
    global bullet_delay
    global game_state
    global music
    global score
    global highscore
    global hit
    global bullet
    global enemy
    global enemy_wave
    global enemy_images
    global heartactive
    global heart_timer
    global heart
    global hearts
    global game_music
    
    

    #gamestate 0 = titlescreen
    #gamestate 1 = main game
    #gamestate 2 = game over screen
    #gamestate 3 = win screen
        
    #game start from title screen
    if game_state ==0:
        if keyboard.e:
            game_state = 1


    #basic movement and barriers
    if keyboard.a:
        if ship.x < -50:
            ship.x = 800
        ship.x = ship.x - 10
    if keyboard.d:
        if ship.x > 800: 
            ship.x = -50
        ship.x = ship.x + 10
    if keyboard.w:
        if ship.y <= 0:
            ship.y = 0
        ship.y = ship.y - 10
    if keyboard.s:
        if ship.y >= 600: 
            ship.y = 600
        ship.y = ship.y + 10
        
    
    
    #backround scrolling
    scroll1.y += scroll_speed
    scroll2.y += scroll_speed
        
    if scroll1.y > HEIGHT*1.5:
        scroll1.y = 0-HEIGHT/2
    if scroll2.y > HEIGHT*1.5:
        scroll2.y = 0-HEIGHT/2
    
    #waves
    if score == 300:
        enemy_wave = 2
    if score == 600:
        enemy_wave = 3
    if score == 900:
        enemy_wave = 4
    
    #bullets firing
    if keyboard.space and bullet_delay == 0 and game_state == 1:
        sounds.gun.play()
        bullet_delay = 16
        bullet = Actor('ammo')
        bullet.x = ship.x
        bullet.y = ship.y
        bullets.append(bullet)
    for bullet in bullets:
        if bullet.y < -35:
            bullets.remove(bullet)
    #bullet movement
    for bullet in bullets:
        bullet.y = bullet.y - 8
        
    for bullet in bullets:
        if bullet.y < 0:
                bullets.remove(bullet) 
    
    #bullet deley    
    if bullet_delay > 0:
        bullet_delay -= 1    
                

    #enemies spawning depending on the wave and movement
    if game_state == 1:
        if random.randint(0, 1000) > 980:
            if enemy_wave == 1:
                enemy = Actor('p-51')
            elif enemy_wave == 2:
                enemy = Actor('jet')
            elif enemy_wave == 3:
                enemy = Actor('jeet')
            else:
                enemy_images = ['p-51', 'jet', 'jeet']
                enemy = Actor(enemy_images[random.randint(0,2)])
            
            enemies.append(enemy)
            enemy.y = -30
            enemy.x = random.randint(50, 750)
        for enemy in enemies:
            if enemy_wave == 1:
                enemy.y += 4
            elif enemy_wave == 2:
                enemy.y += 6
            elif enemy_wave == 3:
                enemy.y += 8
            else:
                enemy.y += 12
                
        for enemy in enemies:
            if enemy.y > 820:
                enemies.remove(enemy)
            
    #enemies colliding with ship
    for enemy in enemies:
            strike = ship.collidelist(enemies)
            if strike != -1:
                enemies.remove(enemies[strike])
                lives = lives - 1
            
    #bullets colliding with enemies    
    for bullet in bullets:
        hit = bullet.collidelist(enemies)
        if hit != -1:
            bullets.remove(bullet)
            enemies.remove(enemies[hit])
            score = score + 10
            
    #heart powerup
    if random.randint(0, 1500) > 1498:
        heart = Actor('heart')
        hearts.append(heart)
        heart.y = -30
        heart.x = random.randint(50, 750)
    for heart in hearts:
        heart.y += 4
    for heart in hearts:
            strike = ship.collidelist(hearts)
            if strike != -1:
                hearts.remove(hearts[strike])
                lives = lives + 1
    
    #dieing
    if game_state ==1:
        if lives <= 0:
            game_state = 2
    
    #respawning
    if game_state == 2:
        if keyboard.e:
            lives = 3
            score = 0
            game_state = 1
            enemies = []
            bullets = []
            enemy_wave = 1
    
    #high score
    if game_state == 2:
        if score > highscore:
            highscore = score

    # Win Screen
    if game_state == 1:
        if score == 1200:
            game_state = 4

        
def draw():
    
    #title screen
    if game_state == 0:
        title_screen.draw()
        screen.draw.text('War  for  Japan', (190,150), color=(255,255,255), fontname = 'arcadeclassic', fontsize=70)
        screen.draw.text('By  BRobertson  studios', (190,210), color=(255,255,255), fontname = 'arcadeclassic', fontsize=50)
        screen.draw.text('Press e to start', (190,250), color=(255,255,255), fontname = 'arcadeclassic', fontsize=30)
    

    
    #game running assests
    if game_state == 1:
        screen.clear()
        screen.fill((128, 0, 0))
    
        scroll1.draw()
        scroll2.draw()
        star.draw()
        
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for heart in hearts:
            heart.draw()
        
        #scoreboard
        screen.draw.text('Score  ' + str(score), (15,10), color=(255,255,255), fontname = 'arcadeclassic', fontsize=30)
        screen.draw.text('HighScore  ' + str(highscore), (15,40), color=(255,255,255), fontname = 'arcadeclassic', fontsize=30)
        screen.draw.text('lives  ' + str(lives) , (15,70), color=(255,255,255), fontname = 'arcadeclassic', fontsize=30)
        screen.draw.text('Wave  ' + str(enemy_wave), (15, 100), color=(255,255,255), fontname = 'arcadeclassic', fontsize = 30)
        screen.draw.text('Move  with  wasd', (570,10), color=(255,255,255), fontname = 'arcadeclassic', fontsize=30)
        
        #game over screen
    if game_state == 2:
        screen.clear()

        screen.draw.text('Score  ' + str(score), (125,175), color=(255,255,255), fontname = 'arcadeclassic', fontsize=70)
        screen.draw.text('HighScore  ' + str(highscore), (125,225), color=(255,255,255), fontname = 'arcadeclassic', fontsize=70)
        screen.draw.text('Press  e  to  play  again', (125,275), color=(255,255,255), fontname = 'arcadeclassic', fontsize=40)

    if game_state == 3:
        screen.clear()

        screen.draw.text('You Win, Congratulations', (125,175), color=(255,255,255), fontname = 'arcadeclassic', fontsize=70)
        screen.draw.text('HighScore  ', + str(highscore), (125,225), color=(255,255,255), fontname = 'arcadeclassic', fontsize=70)
        screen.draw.text('Press e to play again', (125,275), color=(255,255,255), fontname = 'arcadeclassic', fontsize=40) 
        
        


pgzrun.go()