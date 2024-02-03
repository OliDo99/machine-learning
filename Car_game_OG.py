import pygame
import math
CAR_IMAGE = pygame.transform.scale(pygame.image.load("Images/Car.png"),(50,50))
TRACK = pygame.transform.scale(pygame.image.load("Images/Track_TEST.png"),(1152,648))
FINISH = pygame.transform.scale(pygame.image.load("Images/Finish.png"),(70,100))
SCREEN = pygame.display.set_mode((1152,648))
BORDER_COLOR = (14,209,69)
FPS = 60
run = True

pygame.display.set_caption("NEAT")
class Checkpoint:
    def __init__(self,pos):
        self.img = pygame.transform.scale(pygame.image.load("Images/Finish.png"),(50,300))
        self.mask = pygame.mask.from_surface(self.img)
        self.pos = pos
class AbstractCar:
    
    def __init__(self):
        super().__init__()
        self.img = self.IMG
        self.max_vel = 7
        self.vel = 0
        self.rotation_vel = 4
        self.ang = -90
        self.x, self.y = self.START_POS
        self.acceleration = 0.2
        self.radars = []
        self.alive = True
        self.checkpoint_01 = False
        self.checkpoint_02 = False
        self.finish = False

    def rotate(self, left=False,right=False):
        if left:
            self.ang += self.rotation_vel
        elif right:
            self.ang -= self.rotation_vel
    def draw(self,SCREEN):
        blit_rotate_center(SCREEN,self.img,(self.x-25,self.y-25),self.ang)

    def move_forward(self):
        self.vel = min(self.vel+ self.acceleration, self.max_vel)
        self.move()
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    def move(self):
        radians = math.radians(self.ang)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    def radar(self,radar_ang):
        length = 0
        x = int(self.x)
        y = int(self.y)

        while not SCREEN.get_at((x, y)) == pygame.Color(14, 209, 69) and length < 200:
            length += 1
            x = int(self.x + math.cos(math.radians(self.ang+90+radar_ang)) * length)
            y = int(self.y - math.sin(math.radians(self.ang+90+radar_ang)) * length)

        pygame.draw.line(SCREEN, (255, 255, 255), (self.x,self.y), (x, y), 2)
        pygame.draw.circle(SCREEN, (0, 0, 255, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.x+25 - x, 2)+ math.pow(self.y+25 - y, 2)))
        self.radars.append([radar_ang, dist])
    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            
            input[i] = int(radar[1])
        return input
    def update(self):
        self.radars.clear()
        move_player(self)
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.data()
    def collider(self):
        length = 25
        collision_point_right = [int(self.x + math.cos(math.radians(self.ang+25 )) * length),
                                 int(self.y - math.sin(math.radians(self.ang+25 )) * length)]
        
        collision_point_left = [int(self.x + math.cos(math.radians(self.ang - 25)) * length),
                                int(self.y - math.sin(math.radians(self.ang - 25)) * length)]

        collision_point_right_center = [int(self.x + math.cos(math.radians(self.ang + 90)) * length),
                                        int(self.y - math.sin(math.radians(self.ang + 90)) * length)]

        collision_point_left_center = [int(self.x + math.cos(math.radians(self.ang - 90)) * length),
                                      int(self.y - math.sin(math.radians(self.ang - 90)) * length)]

        collision_point_left_back = [int(self.x + math.cos(math.radians(self.ang+25-180 )) * length),
                                 int(self.y - math.sin(math.radians(self.ang+25-180 )) * length)]
        collision_point_right_back = [int(self.x + math.cos(math.radians(self.ang-25-180 )) * length),
                                 int(self.y - math.sin(math.radians(self.ang-25-180 )) * length)]

        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 5)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 5)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right_center, 5)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left_center, 5)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right_back, 5)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left_back, 5)

        if SCREEN.get_at(collision_point_right) == pygame.Color(14, 209, 69) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_left_center) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_right_center) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_right_back) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_left_back) == pygame.Color(14, 209, 69):
            self.alive = False
            print(self.alive)

        if SCREEN.get_at(collision_point_right) == pygame.Color(195,195,195) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_left_center) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_right_center) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_right_back) == pygame.Color(14, 209, 69)or SCREEN.get_at(collision_point_left_back) == pygame.Color(14, 209, 69):
            self.alive = False
            print(self.alive)
        
        if self.collide(Finish.mask, *Finish.pos) != None and self.finish != True:
            print(f"Finish")
            self.finish = True
        if self.collide(Checkpoint_01.mask, *Checkpoint_01.pos) != None and self.checkpoint_01 != True:
            print(f" Checkpoint 1")
            self.checkpoint_01= True
        if self.collide(Checkpoint_02.mask, *Checkpoint_02.pos) != None and self.checkpoint_02!= True:
            print(f"Checkpoint 2")
            self.checkpoint_02 = True
class PlayerCar(AbstractCar):
    IMG = CAR_IMAGE
    START_POS =(300,90)
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/1, 0)
        self.move()

def blit_rotate_center(SCREEN, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    SCREEN.blit(rotated_image, new_rect.topleft)
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

Finish = Checkpoint((1000,50))
Checkpoint_01 = Checkpoint((300,300))
Checkpoint_02 = Checkpoint((700,20))
images = [(TRACK,(0,0)),(Checkpoint_01.img,Checkpoint_01.pos),(Checkpoint_02.img,Checkpoint_02.pos)]
clock = pygame.time.Clock()


player_car = PlayerCar()
player_car2 = PlayerCar()
cars = [player_car]


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    clock.tick(FPS)
    SCREEN.blit(TRACK, (0, 0))
    
    for car in cars:
        car.draw(SCREEN)
        car.update()
        car.collider()
        car.data()
    pygame.display.update()


pygame.quit()