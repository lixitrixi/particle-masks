import pygame, sys, random, math
from pygame.locals import *
from pygame.math import Vector2 as vec2

class Particle:
    def __init__(self, p:vec2) -> None:
        self.p = p
        self.timer = 0
    
    def update(self):
        self.p += self.get_vel()
        self.timer += 1
    
    def get_vel(self):
        p = self.p
        v = vec2(0,0)

        v.x = -p.y
        v.y = -p.x

        return 0.001*v
    
    def get_color(self):
        try:
            return img_arr[int(self.p.x)][int(self.p.y)]
        except IndexError:
            return (0,)*3
    
    def is_out(self):
        return not pygame.Rect(0, 0, size.x, size.y).collidepoint(*self.p)

def grayscale(img:pygame.Surface) -> pygame.Surface:
    arr = pygame.surfarray.array3d(img)
    arr=arr.dot([0.298, 0.587, 0.114])[:,:,None].repeat(3,axis=2)
    return pygame.surfarray.make_surface(arr)

P_COUNT = 3000 # max particle count
P_TIMEOUT = 1000 # number of frames until particles time out
P_TRAIL_LENGTH = 254 # n of pixels for particle trails to extend,
# 255 means they are permanent

# URL = 'particle-masks/starrynight.jpeg'
URL = 'particle-masks/starrynight.jpeg'

# img = pygame.image.load(URL)
img = pygame.Surface((800,800))
img.fill((255,255,255))

size = vec2(img.get_size())/2
img = pygame.transform.scale(img, size)

# img = grayscale(img)
img_arr = pygame.surfarray.array3d(img)

mask = pygame.Surface(size)
mask.fill((0,)*3)
mask.set_alpha(255-P_TRAIL_LENGTH)

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
particles = []

def main():
    while True:
        for event in pygame.event.get():
            if event.type==QUIT: pygame.quit(), sys.exit()

        if len(particles) < P_COUNT:
            rx = random.random()*size.x
            ry = random.random()*size.y
            c = round(random.random())
            particles.append(Particle(vec2(rx,ry)))
        
        for p in particles:
            p.update()
            if p.is_out():
                particles.remove(p)
            # pygame.draw.rect(screen, p.get_color(), (*p.p, 1, 1))
            pygame.draw.circle(screen, p.get_color(), p.p, 1)
        
        pygame.display.flip()
        screen.blit(mask, (0,0))
        clock.tick()

if __name__ == "__main__":
    main()