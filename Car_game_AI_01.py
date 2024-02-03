import pygame
import neat
import math
import os
import sys
pygame.init()

CAR_IMAGE = pygame.transform.scale(pygame.image.load("Images/Car.png"),(50,50))
TRACK = pygame.transform.scale(pygame.image.load("Images/Track.png"),(1152,648))
SCREEN = pygame.display.set_mode((1152,648))
FPS = 60
clock = pygame.time.Clock()
gen = 0
font = pygame.font.SysFont("arialblack",20)
pygame.display.set_caption("NEAT")

class Car(pygame.sprite.Sprite):
    START_POS =(300,90)
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Images/Car.png"),(50,50))
        self.max_vel = 5
        self.vel = 0
        self.rotation_vel = 5
        self.ang = -90
        self.x, self.y = self.START_POS
        self.acceleration = 0.2
        self.radars = []
        self.rect = self.image.get_rect(center=(25, 25))
        self.alive = True
    def draw(self):
        blit_rotate_center(SCREEN,self.image,(self.x,self.y),self.ang)
    def rotate_left(self):
            self.ang += self.rotation_vel
    def rotate_right(self):
            self.ang -= self.rotation_vel
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def move(self):
        radians = math.radians(self.ang)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    def radar(self,radar_ang):
        length = 0
        x = int(self.x)
        y = int(self.y)

        while not SCREEN.get_at((x, y)) == pygame.Color(14, 209, 69) and length < 200:
            length += 1
            x = int(self.x+25 + math.cos(math.radians(self.ang+90+radar_ang)) * length)
            y = int(self.y+25 - math.sin(math.radians(self.ang+90+radar_ang)) * length)

        #pygame.draw.line(SCREEN, (255, 255, 255, 255), (self.x+25,self.y+25), (x, y), 1)
        #pygame.draw.circle(SCREEN, (0, 0, 255, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.x+25 - x, 2)+ math.pow(self.y+25 - y, 2)))
        self.radars.append([radar_ang, dist])
    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            #print(f"{i} {radar}")
            input[i] = int(radar[1])
        return input
    def update(self):
        self.radars.clear()
        move_player(self)
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.data()
        self.collider()
        self.draw()
    def collider(self):
    
        length = 25
        collision_point_right = [int(self.x+25 + math.cos(math.radians(self.ang + 25+90)) * length),
                                 int(self.y+25 - math.sin(math.radians(self.ang + 25+90)) * length)]
        
        collision_point_left = [int(self.x+25 + math.cos(math.radians(self.ang - 25+90)) * length),
                                int(self.y+25 - math.sin(math.radians(self.ang - 25+90)) * length)]

        collision_point_right_center = [int(self.x+25 + math.cos(math.radians(self.ang + 90+90)) * length),
                                        int(self.y+25 - math.sin(math.radians(self.ang + 90+90)) * length)]

        collision_point_left_center = [int(self.x+25 + math.cos(math.radians(self.ang - 90+90)) * length),
                                int(self.y+25 - math.sin(math.radians(self.ang - 90+90)) * length)]

        collision_point_back = [int(self.x+25 + math.cos(math.radians(self.ang - 90)) * length),
                                int(self.y+25 - math.sin(math.radians(self.ang - 90)) * length)]

        if SCREEN.get_at(collision_point_right) == pygame.Color(14, 209, 69) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_left_center) == pygame.Color(14, 209, 69) or SCREEN.get_at(collision_point_right_center) == pygame.Color(14, 209, 69)or SCREEN.get_at(collision_point_back) == pygame.Color(14, 209, 69):
            self.alive = False

def blit_rotate_center(SCREEN, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    SCREEN.blit(rotated_image, new_rect.topleft)
def move_player(player_car):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_car.rotate_left()
    if keys[pygame.K_d]:
        player_car.rotate_right()
    if keys[pygame.K_w]:

        player_car.move_forward()
    if keys[pygame.K_s]:
        player_car.move_backward()
def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)
def eval_genomes(genomes, config):
    
    global cars, ge, nets
    global gen
    cars = []
    ge = []
    nets = []
    gen += 1
    
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break

        if len(cars) == 0:
            break

        SCREEN.blit(TRACK, (0, 0))

        # text_surface = SCREEN.render(f"Gen {gen}", False, (0, 0, 0))
        # SCREEN.blit(text_surface, (0, 0))


        for i, car in enumerate(cars):
           
            ge[i].fitness += 1

            if not car.sprite.alive:
                remove(i)
     
        for i, car in enumerate(cars):
            car.sprite.move_forward()
            output = nets[i].activate(car.sprite.data())
            
            if output[0] < 0:
                car.sprite.rotate_left()
                
            elif output[1] < 0:
                car.sprite.rotate_right()

        for car in cars:
            car.update()
        text = font.render(f"Genaration: {gen}",True,(0,0,0))
        SCREEN.blit(text,(20,20))
        pygame.display.update()
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 1000)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)