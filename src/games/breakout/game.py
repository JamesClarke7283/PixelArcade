import pygame
import sys
from src.logging import get_logger

logger = get_logger()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 10

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - PADDLE_WIDTH // 2
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = 3
        self.speed_y = -3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        if self.rect.bottom >= SCREEN_HEIGHT:
            return True
        return False

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    logger.info("Starting Breakout game")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")
    
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    
    paddle = Paddle()
    ball = Ball()
    all_sprites.add(paddle, ball)

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick = Brick(col * (BRICK_WIDTH + 2) + 30, row * (BRICK_HEIGHT + 2) + 30)
            all_sprites.add(brick)
            bricks.add(brick)

    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        if ball.update():
            logger.info("Game Over")
            running = False

        if pygame.sprite.collide_rect(ball, paddle):
            ball.speed_y = -ball.speed_y

        brick_collision = pygame.sprite.spritecollide(ball, bricks, True)
        if brick_collision:
            ball.speed_y = -ball.speed_y
            score += len(brick_collision)

        if len(bricks) == 0:
            logger.info("You win!")
            running = False

        screen.fill(BLACK)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    logger.info(f"Breakout game ended. Final score: {score}")

if __name__ == "__main__":
    main()