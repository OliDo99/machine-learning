import pygame
import neat
import math
import os
import sys
pygame.init()
TRACK = pygame.transform.scale(pygame.image.load("Images/Track3.png"),(1152,648))
SCREEN = pygame.display.set_mode((1152,648))
FPS = 60
BORDER_COLOR = (14,209,69)
FINISH_COLOR = (136,0,27)
CHECK_POINT_COLOR_01 = (239,161,93)
CHECK_POINT_COLOR_02 = (185,122,86)
CHECK_POINT_COLOR_03 = (206,157,157)
CHECK_POINT_COLOR_04 = (169,69,21)
CHECK_POINT_COLOR_05 = (255,174,200)
CHECK_POINT_COLOR_06 = (255,127,39)
CHECK_POINT_COLOR_07 = (253,236,166)
CHECK_POINT_COLOR_08 = (192,179,129)
CHECK_POINT_COLOR_09 = (158,84,0)

PLAYER_X = 50
PLAYER_Y = 25
clock = pygame.time.Clock()
gen = 0
best_score = 0
font = pygame.font.SysFont("arialblack",20)
pygame.display.set_caption("NEAT")

class Car(pygame.sprite.Sprite):
    START_POS =(100,100)
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Images/Car2.png"),(PLAYER_X,PLAYER_Y))
        self.max_vel = 5
        self.vel = 0
        self.rotation_vel = 5
        self.ang = -45
        self.x, self.y = self.START_POS
        self.acceleration = 0.2
        self.radars = []
        self.rect = self.image.get_rect(center=(PLAYER_X/2, PLAYER_Y/2))
        self.alive = True
        self.finish = False
        self.time_left = 50
        self.collected = [(CHECK_POINT_COLOR_01,False,False,100),(CHECK_POINT_COLOR_02,False,False,300),(CHECK_POINT_COLOR_03,False,False,500),(CHECK_POINT_COLOR_04,False,False,700),(CHECK_POINT_COLOR_05,False,False,900),(CHECK_POINT_COLOR_06,False,False,120)]
    def draw(self):
        blit_rotate_center(SCREEN,self.image,(self.x-(PLAYER_X/2),self.y-(PLAYER_Y/2)),self.ang)
    def rotate_left(self,rotation_value):
            self.ang += self.rotation_vel*rotation_value
    def rotate_right(self,rotation_value):
            self.ang -= self.rotation_vel*rotation_value
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def move(self):
        radians = math.radians(self.ang-90)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    def const_move(self):
        self.vel = 1
        self.move()
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    def radar(self,radar_ang):
        length = 0
        x = int(self.x)
        y = int(self.y)

        while not SCREEN.get_at((x, y)) == pygame.Color(BORDER_COLOR) and length < 200:
            length += 1
            x = int(self.x+(PLAYER_X/2) + math.cos(math.radians(self.ang+radar_ang)) * length)
            y = int(self.y+(PLAYER_Y/2) - math.sin(math.radians(self.ang+radar_ang)) * length)
        dist = int(math.sqrt(math.pow(self.x+(PLAYER_X/2) - x, 2)+ math.pow(self.y+(PLAYER_Y/2) - y, 2)))
        self.radars.append([radar_ang, dist])
        pygame.draw.line(SCREEN, (255, 255, 255), (self.x,self.y), (x, y), 1)
        pygame.draw.circle(SCREEN, BORDER_COLOR, (x, y), 1)
    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input
    def update(self):
        self.radars.clear()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.data()
        self.collider()
        self.draw()
    def collider(self):
        length = PLAYER_Y
        collision_point_right = [int(self.x + math.cos(math.radians(self.ang+25 )) * length),
                                 int(self.y - math.sin(math.radians(self.ang+25 )) * length)]      
        collision_point_left = [int(self.x + math.cos(math.radians(self.ang - 25)) * length),
                                int(self.y - math.sin(math.radians(self.ang - 25)) * length)]
        collision_point_right_center = [int(self.x + math.cos(math.radians(self.ang + 90)) * length/2),
                                        int(self.y - math.sin(math.radians(self.ang + 90)) * length/2)]
        collision_point_left_center = [int(self.x + math.cos(math.radians(self.ang - 90)) * length/2),
                                      int(self.y - math.sin(math.radians(self.ang - 90)) * length/2)]
        collision_point_left_back = [int(self.x + math.cos(math.radians(self.ang+25-180 )) * length),
                                 int(self.y - math.sin(math.radians(self.ang+25-180 )) * length)]
        collision_point_right_back = [int(self.x + math.cos(math.radians(self.ang-25-180 )) * length),
                                 int(self.y - math.sin(math.radians(self.ang-25-180 )) * length)]
       
        if SCREEN.get_at(collision_point_right) == pygame.Color(BORDER_COLOR) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(BORDER_COLOR) or SCREEN.get_at(collision_point_left_center) == pygame.Color(BORDER_COLOR) or SCREEN.get_at(collision_point_right_center) == pygame.Color(BORDER_COLOR) or SCREEN.get_at(collision_point_right_back) == pygame.Color(BORDER_COLOR) or SCREEN.get_at(collision_point_left_back) == pygame.Color(BORDER_COLOR):
            self.alive = False
        if SCREEN.get_at(collision_point_right) == pygame.Color(FINISH_COLOR) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(FINISH_COLOR) or SCREEN.get_at(collision_point_left_center) == pygame.Color(FINISH_COLOR) or SCREEN.get_at(collision_point_right_center) == pygame.Color(FINISH_COLOR) or SCREEN.get_at(collision_point_right_back) == pygame.Color(FINISH_COLOR) or SCREEN.get_at(collision_point_left_back) == pygame.Color(FINISH_COLOR):
            self.finish = True
        
        for i,key in enumerate(self.collected):
            

            if SCREEN.get_at(collision_point_right) == pygame.Color(self.collected[i][0]) \
                    or SCREEN.get_at(collision_point_left) == pygame.Color(self.collected[i][0]) or SCREEN.get_at(collision_point_left_center) == pygame.Color(self.collected[i][0]) or SCREEN.get_at(collision_point_right_center) == pygame.Color(self.collected[i][0]) or SCREEN.get_at(collision_point_right_back) == pygame.Color(self.collected[i][0]) or SCREEN.get_at(collision_point_left_back) == pygame.Color(self.collected[i][0]):
                
                update_collected = list(self.collected[i])
                update_collected[1] = True
                self.collected[i] = tuple(update_collected)
                

def blit_rotate_center(SCREEN, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    SCREEN.blit(rotated_image, new_rect.topleft)
def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)
def eval_genomes(genomes, config):
    
    global cars, ge, nets
    global gen, best_score
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

        for i, car in enumerate(cars):
           
            ge[i].fitness += 1
            car.sprite.time_left -=1

            if car.sprite.finish:
                ge[i].fitness =1500 - ge[i].fitness
                car.sprite.alive = False

            for l,key in enumerate(car.sprite.collected):
                if car.sprite.collected[l][1] and  not car.sprite.collected[l][2]:
                    ge[i].fitness += key[3] - ge[i].fitness
                    
                    update_collected = list(car.sprite.collected[l])
                    update_collected[2] = True
                    car.sprite.collected[l] = tuple(update_collected)
                    car.sprite.time_left += 50
                    #print(f"Checkpoint:{l} cleared by: {i}")

            if int(ge[i].fitness) >= int(best_score):
                best_score = int(ge[i].fitness)

            if car.sprite.time_left ==0:
                remove(i)
            if not car.sprite.alive:
                remove(i)
     
        for i, car in enumerate(cars):
            
            output = nets[i].activate(car.sprite.data())

            if output[2] < 0:
                car.sprite.move_forward()
                if output[0] < 0:
                    car.sprite.rotate_left(1)         
                if output[1] < 0:
                    car.sprite.rotate_right(1)
            else:
                car.sprite.const_move()
                if output[0] < 0:
                    car.sprite.rotate_left(0.5)         
                if output[1] < 0:
                    car.sprite.rotate_right(0.5)
            
            

        for car in cars:
            car.update()
             
        text_alive = font.render(f"Alive: {len(ge)}",True,(0,0,0))
        text_gen = font.render(f"Genaration: {gen}",True,(0,0,0))
        text_score = font.render(f"Best score: {best_score}",True,(0,0,0))
        SCREEN.blit(text_alive,(950,20))
        SCREEN.blit(text_gen,(750,20))
        SCREEN.blit(text_score,(550,20))
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