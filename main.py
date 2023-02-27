import pygame, random
from pygame.math import Vector2
from sys import exit

class Fruit:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size,cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen, pygame.Color("green"), block_rect)

    def move_snake(self):
        if self.new_block == False:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy
        else:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy
            self.new_block = False
        
    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]

class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.randomize()
            self.snake.add_block()
            for block in self.snake.body:
                if self.fruit.pos == block:
                    x=True
                else:
                    x=False
            while x == True:
                self.fruit.randomize()
                for block in self.snake.body:
                    if self.fruit.pos == block:
                        x=True
                    else:
                        x=False

    def check_fail(self):
        if not 0 <= self.snake.body[0].x <= 19 or not 0 <= self.snake.body[0].y <= 19:
            self.game_over()
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()
        
    def game_over(self):
        self.snake.reset()

    def draw_score(self):
        score_text = str(f"Score: {len(self.snake.body)-3}")
        score_surface = game_font.render(score_text, True, (255,255,255))
        score_x = cell_number*cell_size - 80
        score_y = 25
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface, score_rect)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
apple = pygame.image.load("apple.png").convert_alpha()
DEFAULT_IMAGE_SIZE = (40, 40)
apple = pygame.transform.scale(apple, DEFAULT_IMAGE_SIZE)
game_font = pygame.font.Font("Smack Boom.ttf", 25)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_s and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_a and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_d and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1,0)
    screen.fill((0,0,0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
