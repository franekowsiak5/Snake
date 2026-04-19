import pygame
import sys
import random

pygame.init()
pygame.font.init()

width,height=500,500


font = pygame.font.SysFont('Arial', 32)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake")

body = pygame.image.load("body.png").convert()
body.set_colorkey((255, 255, 255))
head = pygame.image.load("head.png").convert()
head.set_colorkey((255, 255, 255))
apple = pygame.image.load("apple.png").convert()
apple.set_colorkey((255, 255, 255))
clock_tick = 4

class Level:
    def __init__(self,amount_w,amount_h):
        self.amount_w = amount_w
        self.amount_h = amount_h
    
    # rysowanie planszy,
    # jeżeli kwadrawty nie wyhodzą kwadratowe- rysuje biały margines po lewej i prawej
    def draw_map(self):
        size_h = int(height/self.amount_h)
        size_w = int(width/self.amount_w)
        margin_h, margin_w = 0,0
        
        # adding margins
        if size_h > size_w:
            size_h = size_w
            margin_h = (height - (size_h * self.amount_h)) / 2
            if size_w < width/self.amount_w:
                margin_w += (width - (size_w * self.amount_w)) / 2
        else:
            size_w = size_h
            margin_w = (width - (size_w * self.amount_w)) / 2
            if size_h < height/self.amount_h:
                margin_h += (height - (size_h * self.amount_h)) / 2

        self.size_w = size_w
        self.size_h = size_h
        self.margin_w = margin_w
        self.margin_h = margin_h
        
        body_scaled = pygame.transform.scale(body,(size_w, size_h))
        head_scaled = pygame.transform.scale(head,(size_w, size_h))
        apple_scaled = pygame.transform.scale(apple,(size_w, size_h))
        
        self.body_scaled = body_scaled
        self.head_scaled = head_scaled
        self.apple_scaled = apple_scaled
        
        for y in range(self.amount_h):
            for x in range(self.amount_w):
                if (x+y) % 2 == 0:
                    pygame.draw.rect(screen,(0,255,127),((size_w * x) + margin_w, (size_h * y) + margin_h ,size_w, size_h)) 
                else:
                    pygame.draw.rect(screen,(60,179,113),((size_w * x) + margin_w, (size_h * y) + margin_h, size_w, size_h))

Level1= Level(10,10)

snake = [(3, 5), (2, 5), (1, 5)]  #(x, y), pierwszy to glowa
direction = (1, 0)  #(dx, dy)
next_direction = (1, 0)
food = (7, 5)

def generate_food(snake, amount_w, amount_h):
    while True:
        food_pos = (random.randint(0, amount_w - 1), random.randint(0, amount_h - 1))
        if food_pos not in snake:
            return food_pos

food = generate_food(snake, Level1.amount_w, Level1.amount_h)
score = 0
game_over = False


def draw_snake(snake, size_w, size_h, margin_w, margin_h):
    for i, segment in enumerate(snake):
        x, y = segment
        pos_x = (x * size_w) + margin_w
        pos_y = (y * size_h) + margin_h
        
        if i == 0: 
            screen.blit(Level1.head_scaled, (pos_x, pos_y))
        else: 
            screen.blit(Level1.body_scaled, (pos_x, pos_y))


def draw_food(food, size_w, size_h, margin_w, margin_h):
    x,y = food
    screen.blit(Level1.apple_scaled, (x * size_w + margin_w, y * size_h + margin_h))


def update_game():
    global snake, food, score, game_over, direction, next_direction
    

    if next_direction != (0, 0):
        if (next_direction[0] * -1, next_direction[1] * -1) != direction:
            direction = next_direction
    
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    

    if new_head == food: #dodaje kolejne
        snake.insert(0, new_head)
        score += 1
        food = generate_food(snake, Level1.amount_w, Level1.amount_h)
    else: #dodaje kolejne ale usuwa ostatnie
        snake.insert(0, new_head)
        snake.pop()
    

    head = snake[0]
    if (head[0] < 0 or head[0] >= Level1.amount_w or 
        head[1] < 0 or head[1] >= Level1.amount_h):
        game_over = True

    if head in snake[1:]:
        game_over = True

def record_score(score):
    with open("scores.txt", "r") as file:
        high_score = file.readlines()[0]
    if score > int(high_score):
        with open("scores.txt", "w") as file:
            file.write(f"{score}\n")

def restart_game():
    global snake, direction, next_direction, food, score, game_over
    snake = [(3, 5), (2, 5), (1, 5)]
    direction = (1, 0)
    next_direction = (1, 0)
    food = generate_food(snake, Level1.amount_w, Level1.amount_h)
    score = 0
    game_over = False

main_menu = True
while main_menu:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            main_menu = False
    screen.fill((128,128,128))
    title_text = font.render("Snake Game", True, (0, 255, 0))
    instruction_text = font.render("Press any key to start", True, (0, 255, 0))
    title_rect = title_text.get_rect(center=(width/2, height/2 - 20))
    instruction_rect = instruction_text.get_rect(center=(width/2, height/2 + 20))
    score_text = font.render(f"High Score: {open('scores.txt', 'r').readlines()[0].strip()}", True, (0, 255, 0))
    score_rect = score_text.get_rect(center=(width/2, height/2 + 60))
    Level1.draw_map()
    draw_food(food, Level1.size_w, Level1.size_h, Level1.margin_w, Level1.margin_h)
    draw_snake(snake, Level1.size_w, Level1.size_h, Level1.margin_w, Level1.margin_h)
    pygame.draw.rect(screen, (120, 120, 120), (title_rect.x - 10, title_rect.y - 100, title_rect.width + 20, title_rect.height + 20))
    pygame.draw.rect(screen, (120, 120, 120), (instruction_rect.x - 10, instruction_rect.y - 100, instruction_rect.width + 20, instruction_rect.height + 20))
    pygame.draw.rect(screen, (120, 120, 120), (score_rect.x - 10, score_rect.y - 100, score_rect.width + 20, score_rect.height + 20))
    screen.blit(title_text, (title_rect.x, title_rect.y - 90))
    screen.blit(instruction_text, (instruction_rect.x, instruction_rect.y - 90))
    screen.blit(score_text, (score_rect.x, score_rect.y - 90))
    
    pygame.display.flip()
    

while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)
            if event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)
            if event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)
            if event.key == pygame.K_w:
                clock_tick += 5
            if event.key == pygame.K_s and clock_tick > 5:
                clock_tick -= 5

            
        

        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                restart_game()

    screen.fill((128,128,128))
    
    Level1.draw_map()


    

    if not game_over:
        update_game()
    

    draw_food(food, Level1.size_w, Level1.size_h, Level1.margin_w, Level1.margin_h)
    draw_snake(snake, Level1.size_w, Level1.size_h, Level1.margin_w, Level1.margin_h)
    
    score_text = font.render(f"Wynik: {score}", True, (0,0,0))
    screen.blit(score_text, (10, 10))
    

    if game_over:
        record_score(score)
        game_over_text = font.render("gameover, R-Restart", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(width/2, height/2))
        screen.blit(game_over_text, text_rect)
        
        final_score_text = font.render(f"wynik: {score}", True, (255, 255, 255))
        final_rect = final_score_text.get_rect(center=(width/2, height/2 + 40))
        screen.blit(final_score_text, final_rect)

    pygame.display.flip()

    clock.tick(clock_tick)