"""
bounce.py 
Simple bouncing balls using pygame

Problems:
    Multiple collsions handled poorly
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random
import pygame as pg


CAPTION = "Bounce 04"
SCREEN_SIZE = (400, 400)
BALL_SIZE = 20
BALL_COUNT = 20
MAX_FPS = 30
DETAIL = False
COLLIDE_DETAIL = False

from pygame.locals import ( K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,)



class Body(pg.sprite.Sprite):
    def __init__(self, x, y, vx, vy, n):
        super(Body, self).__init__()
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill( Body.rand_fill() )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        class _vel:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        self.vel = _vel(vx, vy)
        self.n = n
        self.bounced = False

    def rand_fill():
        return random.choice( [
            pg.Color("brown"), pg.Color("red"), pg.Color("orange"),
            pg.Color("yellow"), pg.Color("green"), pg.Color("blue"),
            pg.Color("violet"), pg.Color("gray"), pg.Color("white"), ])

    def ball_collision(sprite1, sprite2):
        if sprite1 is not sprite2:
            return sprite1.rect.colliderect(sprite2.rect)
        else:
            return False


    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        if self.rect.x <= 0: 
            self.rect.x = 0
            self.vel.x = -self.vel.x
        elif self.rect.x >= SCREEN_SIZE[0]-BALL_SIZE: 
            self.rect.x = SCREEN_SIZE[0]-BALL_SIZE
            self.vel.x = -self.vel.x
        if self.rect.y <= 0: 
            self.rect.y = 0
            self.vel.y = -self.vel.y
        elif self.rect.y >= SCREEN_SIZE[1]-BALL_SIZE: 
            self.rect.y = SCREEN_SIZE[1]-BALL_SIZE
            self.vel.y = -self.vel.y
        self.bounced = False

    def process_collision(self, tgt):
        if self.bounced: return
        self.bounced = True
        xbounce = False
        if self.rect.right >= tgt.rect.left and self.rect.right <= tgt.rect.right:
            oldx = self.vel.x
            self.vel.x, tgt.vel.x = tgt.vel.x, self.vel.x 
            xbounce = True
        elif self.rect.left <= tgt.rect.right and self.rect.left >= tgt.rect.right:
            self.vel.x, tgt.vel.x = tgt.vel.x, self.vel.x 
            xbounce = True

        ybounce = False
        if self.rect.bottom >= tgt.rect.top and self.rect.bottom <= tgt.rect.bottom:
            self.vel.y, tgt.vel.y = tgt.vel.y, self.vel.y 
            ybounce = True
        elif self.rect.top <= tgt.rect.bottom and self.rect.top >= tgt.rect.bottom:
            self.vel.y, tgt.vel.y = tgt.vel.y, self.vel.y 
            ybounce = True

        if xbounce or ybounce:
            tgt.bounced = True




def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()

    balls = pg.sprite.Group()
    # x test
    #balls.add( Body(100, 100,  7, 0, 0) )
    #balls.add( Body(200,  88, -1, 0, 1) )
    #balls.add( Body(200, 112, -3, 0, 1) )

    #y test
    #balls.add( Body(300, 100,  0,-3, 3) )
    #balls.add( Body(300, 200,  0, 4, 4) )

    #big random
    n = 0
    for j in range(BALL_SIZE, SCREEN_SIZE[0], (5*BALL_SIZE)):
        for k in range(BALL_SIZE, SCREEN_SIZE[1], (5*BALL_SIZE)):
            balls.add( Body (j, k, random.randint(-2,3), random.randint(-2,3),  n) )
            n += 1


    running = True
    update = True

    while running:
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                else:
                    update = True

            elif event.type == QUIT:
                running = False

        update = True
        if update:
            screen.fill(pg.Color("black"))

            balls.update()
            
            hits = pg.sprite.groupcollide(
                    balls, balls,
                    False, False, collided=Body.ball_collision)
            if hits:
                for h,L in hits.items():
                    h.process_collision(L[0])
                    #print (h.n, len(L), [x.n for x in L])
                #print ("="*20)

            balls.draw(screen)


            pg.display.update()
            pg.display.flip()

            update = False
    
        clock.tick_busy_loop(MAX_FPS)
    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
