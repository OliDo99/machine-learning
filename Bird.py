import pygame
import random
import math
pygame.init()
pygame.display.set_caption("NEAT")
SCREEN = pygame.display.set_mode((1200,700))
FPS = 60
BIRD_COLOR = (255,255,0)
PIPE_COLOR = (0,50,200)
GROUND_COLOR = (100,100,100)
BLUE_COLOR = (0, 255, 255, 0)
BG_COLOR = (10,10,10)
FONT = pygame.font.SysFont("arialblack",20)
CLOCK = pygame.time.Clock()
START = pygame.time.get_ticks()

class Bird():
    def __init__(self):
        self.alive = True
        self.len = 30
        self.x = 200
        self.y = 100
        self.g = 10
        self.jump_vel = 30
        self.dir = 0 
        self.max_vel = 50
        self.radar = [-180,-135,-90,-45,0,45,90,135]
    def gravity(self):
        if self.dir < self.max_vel:
            self.dir +=  self.g * 0.2
        self.y += self.dir * 0.2
    def jump(self):
        if self.y >0:
            self.dir = - self.jump_vel
    def draw(self):
        pygame.draw.circle(SCREEN, BIRD_COLOR, (self.x, self.y), self.len)
    def collider(self):
        for i in self.radar:
            color = SCREEN.get_at([int(self.x + math.cos(math.radians(i)) * self.len),int(self.y - math.sin(math.radians(i)) * self.len)])
            if color == PIPE_COLOR or color == GROUND_COLOR:
                self.alive =False
class Pipe():
    def __init__(self):
        self.color = PIPE_COLOR
        self.center = [(1200,random.randint(150,600))]
        self.vel = 5
    def move(self):
        for i in range(len(self.center)):
            
            self.center[i] =  (self.center[i][0] - self.vel, self.center[i][1])
    def draw(self):
        for i in range(len(self.center)):
            pygame.draw.polygon(SCREEN,self.color,((self.center[i][0],self.center[i][1] + 100),(self.center[i][0] + 100,self.center[i][1] + 100),(self.center[i][0]+100,700),(self.center[i][0],700)))
            pygame.draw.polygon(SCREEN,self.color,((self.center[i][0],self.center[i][1] - 100),(self.center[i][0] + 100,self.center[i][1] - 100),(self.center[i][0]+100,0),(self.center[i][0],0)))
    def newPipe(self):
        num2 = random.randint(150,600)
        self.center.append((1200,num2))
    def delete(self):
            if self.center[0][0] <= -100:
                self.center.pop(0)

def drawLine():
    pygame.draw.line(SCREEN,(255,0,0),(bird.x+0,bird.y+30),(bird.x+0,pipe.center[0][1]+100))
    pygame.draw.line(SCREEN,(255,0,0),(bird.x+0,pipe.center[0][1]+100),(pipe.center[0][0],pipe.center[0][1]+100))
    
    pygame.draw.line(SCREEN,(255,0,0),(bird.x+0,bird.y-30),(bird.x+0,pipe.center[0][1]-100))
    pygame.draw.line(SCREEN,(255,0,0),(bird.x+0,pipe.center[0][1]-100),(pipe.center[0][0],pipe.center[0][1]-100))

    pygame.draw.line(SCREEN,(0,255,0),(bird.x+30,bird.y),(bird.x+30,pipe.center[0][1]))
    pygame.draw.line(SCREEN,(0,255,0),(bird.x+30,pipe.center[0][1]),(pipe.center[0][0],pipe.center[0][1]))
bird = Bird()
pipe = Pipe()

while bird.alive:
    Score = pygame.time.get_ticks()
    CLOCK.tick(FPS)
    SCREEN.fill(BG_COLOR)
    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bird.alive = False
            break
    if keys[pygame.K_w]:
        bird.jump()
    if START + 2000 <= now:
        pipe.newPipe()
        START = now

    SCREEN.fill(BG_COLOR)
    bird.gravity() 
    bird.draw()
    pipe.delete()
    pipe.move()
    pipe.draw()
    drawLine()
    pygame.draw.rect(SCREEN, GROUND_COLOR,(0, 0, 1200, 10))
    pygame.draw.rect(SCREEN, GROUND_COLOR,(0, 690, 1200, 10))

    Score_text = FONT.render(f"Score: {Score}",True,(255,255,255))
    SCREEN.blit(Score_text,(950,20))

    bird.collider()
   
    pygame.display.update()