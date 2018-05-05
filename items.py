class Bullet:
    def __init__(self, x, y, target_x, target_y):
        #loads image of bullet
        self.image = image.load('resources/player/sniper_bullet.png').convert_alpha()
        # x is the x position of the bullet        
        self.x = x
        # y is the y position of the bullet
        self.y = y
        # originalx is the original x position of the bullet, 
        self.originalx = x
        # originaly is the original y position of the bullet, 
        self.originaly = y
        # target_x is where the bullet is going to, 
        self.target_x = target_x
        # target_y is the where the bullet is going to, 
        self.target_y = target_y
        # vel is the velocity that the bullet moves at
        self.vel = 20
        # rnge is the range of the bullet, in frames
        self.rnge = 50
        # prog is the progress of the bullet, in frames
        self.prog = 0
        # dmg is the damage that the bullet will do upon impact
        self.dmg = 1 
        self.dmg_mult = 1
        # deathtick is the timer for enemy death
        self.deathTick = 0
        # rect is the hitbox of the bullet
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def update(self):
        # Increases Progress of the bullet
        try:
            self.x += int((self.vel + pl.shotSpeed_upG) * (self.target_x - self.originalx) /
                          (sqrt((self.target_x - self.originalx) ** 2 +
                                     (self.target_y - self.originaly) ** 2)))
            self.y += int((self.vel + pl.shotSpeed_upG) * (self.target_y - self.originaly) /
                          (sqrt((self.target_x - self.originalx) ** 2 +
                                     (self.target_y - self.originaly) ** 2)))
        except: pass #catches divide by zero errors
        
        self.rect.center = [self.x, self.y]
    
    def check(self, enemies):
        # Checks if the bullet is out of range, then deletes it, if it is
        if self.prog >= self.rnge:
            bullets.remove(self)
        #checks if bullets are out of bounds
        elif not 0 < self.x < WIDTH - self.w or not 0 < self.y < HEIGHT - self.h:
            bullets.remove(self)
            
        else:    
            #checks if bullet hits target hitbox, if so, starts a timer that kills the bullet after 1 frame
            for e in enemies:
                if self.rect.colliderect(e.hitbox):
                    self.deathTick += 1
            
            if bossFight and self.rect.colliderect(bs.rect):
                self.deathTick += 1
            
            if self.deathTick > 1:
                bullets.remove(self)
     
    #draws each bullet      
    def draw(self):
        screen.blit(self.image, self.rect)
        
    #displays current bullet picture in top-left 
    def display(self):
        screen.blit(self.image, Rect(15, 45, self.w * 5, self.h * 5))        
    
    #draws bullet hitboxes
    def debug(self):
        draw.rect(screen, (0,0,0), self.rect, 2)  
        draw.line(screen, (255,255,255), (self.x, self.y), (self.target_x, self.target_y), 4)

class Gattling(Bullet):
    # very fast fire rate, low damage bullet (never used in final version)
    def __init__(self, x, y, target_x, target_y):
        Bullet.__init__(self, x, y, target_x, target_y)
        self.image = image.load('resources/player/gattling_bullet.png').convert_alpha()
        self.hold = True
        self.vel = 20
        self.rnge = 20
        self.dmg = 2     
        self.dmg_mult = 0.5
        self.firing_speed = 1 #ticks before allowed to fire again (1000 ticks in a second)
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.rect = Rect(self.x, self.y, self.w, self.h)        

class Sniper(Bullet):
    #normal bullet
    def __init__(self, x, y, target_x, target_y):
        Bullet.__init__(self, x, y, target_x, target_y)
        self.image = image.load('resources/player/sniper_bullet.png').convert_alpha()
        self.hold = False
        self.vel = 20
        self.rnge = 50 
        self.dmg = 30
        self.dmg_mult = 1        
        self.firing_speed = 333 #ticks before allowed to fire again (1000 ticks in a second)
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.rect = Rect(self.x, self.y, self.w, self.h)      


class EnemyBullet(Bullet):
    #these bullets are fired only by enemies
    def __init__(self, x, y, target_x, target_y, damage = 100):
        Bullet.__init__(self, x, y, target_x, target_y)
        self.image = image.load('resources/enemies/enemy_bullet.png').convert_alpha()
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.rect = Rect(self.x, self.y, self.w, self.h)        
        self.hold = False
        self.vel = 10
        self.rnge = 90
        self.dmg = damage
        
    def check(self, playerHitbox):
        # Checks if the bullet is out of range, then deletes it, if it is
        if self.prog >= self.rnge:
            enemyBullets.remove(self)
        
        elif not 0 < self.x < WIDTH or not 0 < self.y < HEIGHT:
            enemyBullets.remove(self) 
            
        #checks if bullet hits target hitbox, if so, starts a timer that kills the bulle after 1 frame
        elif self.rect.colliderect(playerHitbox):
            self.deathTick += 1

        if self.deathTick > 1:
            enemyBullets.remove(self)    

class Heart():
    #basic heart pickup
    def __init__(self, x, y, hp):
        #image and position (image scales to hp value)
        self.image = transform.scale(image.load('resources/items/heart.png').convert_alpha(), (int((hp / 1000) * image.load('resources/items/heart.png').get_width() * 2), int((hp / 1000) * image.load('resources/items/heart.png').get_height() * 2)))
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.hp = hp
        self.life_span = 300
        self.health = 0
        
    def update(self, player):
        self.health += 1
        #checks if it's supposed to die, if so, dies.
        if self.health >= self.life_span:
            pickups.remove(self)
        
        #checks if player touched it, if so, grants player health, and keels over (if granted health makes player health go over limit, adds however much it can before the limit is reached)
        if self.rect.colliderect(player.hitbox):
            if player.health < player.max_health:
                for hUp in range(self.hp):
                    player.health += 1
                    if player.health >= player.max_health:
                        break
            else:
                player.health = 1000
            pickups.remove(self)
    
    #draws self
    def draw(self):
        screen.blit(self.image, self.rect)
        
