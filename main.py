import pygame
import os
import random
# Initialize Pygame
pygame.init()
# Constants
FIRST_PLANE_COLOUR = (255, 161, 28)
BACKGROUND_COLOUR = (16, 16, 16)
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
def load_images(folder, prefix, count, extension):
    return [pygame.image.load(os.path.join(folder, f"{prefix}{i}.{extension}")) for i in range(1, count + 1)]

RUNNING = load_images("Assets/Dino", "DinoRun", 2, "png")
DUCKING = load_images("Assets/Dino", "DinoDuck", 2, "png")
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DEAD = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))
GAME_OVER = pygame.image.load(os.path.join("Assets/Other", "GameOver.png"))
RESET = pygame.image.load(os.path.join("Assets/Other", "Reset.png"))
SMALL_CACTUS = load_images("Assets/Cactus", "SmallCactus", 3, "png")
LARGE_CACTUS = load_images("Assets/Cactus", "LargeCactus", 3, "png")
BIRD = load_images("Assets/Bird", "Bird", 2, "png")
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
TRACK = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
DRONE = pygame.image.load(os.path.join("Assets/Other", "Drone.png"))
LOGO = pygame.image.load(os.path.join("Assets/Other", "LogoRaptors.png"))

# Game variables
game_speed = 20
points = 0
obstacles = []

# Classes
class Dinosaur:
    X_POSITION = 80
    Y_POSITION = SCREEN_HEIGHT // 2
    Y_DUCK_POSITION = SCREEN_HEIGHT // 2 + 30
    JUMP_VEL = 7.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DEAD

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_dead = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POSITION
        self.dino_rect.y = self.Y_POSITION

    def update(self, userInput):
        if self.dino_dead:
            self.dead()
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE] or userInput[pygame.K_RETURN]) and self.dino_rect.y==self.Y_POSITION and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POSITION
        self.dino_rect.y = self.Y_DUCK_POSITION
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POSITION
        self.dino_rect.y = self.Y_POSITION
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def dead(self):
        self.image = self.dead_img
        self.dino_rect.y += 15

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0, 2000)
        self.y = random.randint(50, SCREEN_HEIGHT // 2 - 60)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed / 5
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(0, 1500)
            self.y = random.randint(50, SCREEN_HEIGHT // 2 - 60)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Drone:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0, 2000)
        self.y = random.randint(50, SCREEN_HEIGHT // 2 - 60)
        self.image = DRONE
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed / 5
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(0, 1500)
            self.y = random.randint(SCREEN_HEIGHT//5, SCREEN_HEIGHT // 2 - 60)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = SCREEN_HEIGHT // 2 + 25


class LargeCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = SCREEN_HEIGHT // 2


class Bird(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = SCREEN_HEIGHT // 2 - 60
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


class Track:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = SCREEN_HEIGHT // 2 + 80

    def draw(self, SCREEN):
        image_width = TRACK.get_width()
        SCREEN.blit(TRACK, (self.x_pos, self.y_pos))
        SCREEN.blit(TRACK, (image_width + self.x_pos, self.y_pos))
        if self.x_pos <= -image_width:
            SCREEN.blit(TRACK, (image_width + self.x_pos, self.y_pos))
            self.x_pos = 0
        self.x_pos -= game_speed

def bestscore(is_first_game):
    global best_score, points
    best_score = 0
    if os.path.exists("best_score.txt"):
        with open("best_score.txt", "r") as file:
            best_score = int(file.readline())
    if not is_first_game:
        if points > best_score:
            best_score = points
            with open("best_score.txt", "w") as file:
                file.write(str(best_score) + '\n')
                print("Updated Best Score:", best_score)
def score():
    global points, game_speed, best_score
    points += 1
    game_speed += 0.05
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Best Score: " + str(best_score) + " / Score: " + str(int(points)), True,
                       FIRST_PLANE_COLOUR)
    textRect = text.get_rect()
    textRect.center = (1000, 40)
    SCREEN.blit(text, textRect)
    if points >= best_score:
        best_score = points


def generate_obstacle(is_):
    global obstacles
    new_obstacle = None

    while new_obstacle is None or any(obstacle.rect.colliderect(new_obstacle.rect) for obstacle in obstacles):
        choice = random.randint(0, 2)
        if choice == 0:
            new_obstacle = SmallCactus(SMALL_CACTUS)
        elif choice == 1:
            new_obstacle = LargeCactus(LARGE_CACTUS)
        elif choice == 2:
            new_obstacle = Bird(BIRD)

    obstacles.append(new_obstacle)


def game():
    global game_speed, points, obstacles
    clock = pygame.time.Clock()
    dinosaur = Dinosaur()
    clouds = [Cloud() for _ in range(9)]
    dron = Drone()
    clouds.append(dron)
    track = Track()
    game_speed = 20
    points = 0
    obstacles = []
    jump_cooldown = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bestscore(False)
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bestscore(False)
                    return False

        SCREEN.fill((16, 16, 16))
        SCREEN.blit(LOGO, (10, SCREEN_HEIGHT - 200))
        userInput = pygame.key.get_pressed()
        track.draw(SCREEN)
        for cloud in clouds:
            cloud.update()
            cloud.draw(SCREEN)

        if len(obstacles) == 0:
            choice = random.randint(0, 2)
            if choice == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif choice == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif choice == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)
            if dinosaur.dino_rect.colliderect(obstacle.rect):
                dinosaur.dino_dead = True
                dinosaur.dino_run = False
                dinosaur.dino_duck = False
                dinosaur.dino_jump = False

                dinosaur.update(userInput)
                dinosaur.draw(SCREEN)
                SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 70))
                SCREEN.blit(RESET, (SCREEN_WIDTH // 2 - 34, SCREEN_HEIGHT // 2))
                score()
                pygame.display.update()
                bestscore(False)
                return True

        dinosaur.update(userInput)
        dinosaur.draw(SCREEN)
        score()

        clock.tick(30)
        pygame.display.update()


def menu(is_first_game):
    global points
    if is_first_game:
        SCREEN.fill(BACKGROUND_COLOUR)
        SCREEN.blit(LOGO, (10, SCREEN_HEIGHT - 200))
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press the space bar to start the game", True, FIRST_PLANE_COLOUR)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_RETURN:
                    if game() == False:
                        return
                    break
                if event.key == pygame.K_ESCAPE:
                    return


if __name__ == "__main__":
    bestscore(True)
    menu(True)
    bestscore(False)
