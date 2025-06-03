import pygame
import sys
import random
import time

WIDTH, HEIGHT = 1000, 600
BLOCK_SIZE = 20
FPS = 15


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TURQUOISE = (64, 224, 208)
LIME = (0, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)

        # Load start screen image
        self.start_image = pygame.image.load(r"D:\final Games code\sanke - game\game starting image\snakeapple.webp")
        self.start_image = pygame.transform.scale(self.start_image, (WIDTH, HEIGHT))

        # Load images for head, body, and tail
        self.head_image = pygame.image.load(r"D:\final Games code\sanke - game\snake image\SNAKE2.jpeg")
        self.head_image = pygame.transform.scale(self.head_image, (BLOCK_SIZE, BLOCK_SIZE))

        self.body_image = pygame.image.load(r"D:\final Games code\sanke - game\snake image\body.png")
        self.body_image = pygame.transform.scale(self.body_image, (BLOCK_SIZE, BLOCK_SIZE))

        self.tail_image = pygame.image.load(r"D:\final Games code\sanke - game\snake image\tail.jpg")
        self.tail_image = pygame.transform.scale(self.tail_image, (BLOCK_SIZE, BLOCK_SIZE))

        # Load apple image
        self.apple_image = pygame.image.load(r"D:\final Games code\sanke - game\snake image\OIP.jpeg")
        self.apple_image = pygame.transform.scale(self.apple_image, (BLOCK_SIZE, BLOCK_SIZE))

        # Load background image
        self.background_image = pygame.image.load(r"D:\final Games code\sanke - game\snake image\back ground.jpeg")
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        # Load background music
        pygame.mixer.music.load(r"D:\final Games code\sanke - game\snake sounds\game-music-loop.mp3")
        pygame.mixer.music.play(-1)

        # Load game over sound
        self.game_over_sound = pygame.mixer.Sound(r"D:\final Games code\sanke - game\snake sounds\game-over-2 waw.wav")  # Replace with your sound file

        self.reset()

    def reset(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()
        self.score = 0

    def generate_apple(self):
        return (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))
        
        # Draw the snake
        for i, (x, y) in enumerate(self.snake):
            if i == len(self.snake) - 1:  # Head
                self.screen.blit(self.head_image, (x, y))
            elif i == 0:  # Tail
                self.screen.blit(self.tail_image, (x, y))
            else:  # Body
                self.screen.blit(self.body_image, (x, y))

        # Draw the apple
        self.screen.blit(self.apple_image, self.apple)

        # Draw score
        text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (15, 15))

    def game_over(self):
        # Play game over sound
        self.game_over_sound.play()

        self.screen.fill(TURQUOISE)
        game_over_text = self.font.render('Game Over', True, RED)
        restart_text = self.font.render('Press R to Restart', True, BLACK)
        final_score_text = self.font.render(f'Final Score: {self.score}', True, PURPLE)
        self.screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
        self.screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 55))
        self.screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
        pygame.display.update()
        time.sleep(5)

    def credits(self):
        self.screen.fill(TURQUOISE)
        credits_text = self.font.render('Made by Aniket Sundriyal', True, BLACK)
        self.screen.blit(credits_text, (WIDTH // 2 - 110, HEIGHT // 3))
        pygame.display.update()
        time.sleep(5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'
                elif event.key == pygame.K_r:
                    self.reset()

    def update(self):
        head = self.snake[-1]
        if self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])
        self.snake.append(new_head)
        if self.snake[-1] == self.apple:
            self.score += 1
            self.apple = self.generate_apple()
        else:
            self.snake.pop(0)
        # Check for collisions
        if (self.snake[-1][0] < 0 or self.snake[-1][0] >= WIDTH or
            self.snake[-1][1] < 0 or self.snake[-1][1] >= HEIGHT or
            self.snake[-1] in self.snake[:-1]):
            self.game_over()
            self.credits()
            self.reset()

    def show_start_screen(self):
        # Draw the start screen image
        self.screen.blit(self.start_image, (0, 0))

        # Draw the start text on top of the image
        start_text = self.font.render('Press Enter to Start', True, WHITE)
        self.screen.blit(start_text, (WIDTH // 2 - 120, HEIGHT // 2 + 250))  # Adjust position

        pygame.display.update()  # Update the screen

        # Wait for user to press Enter
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Check for Enter key
                        waiting = False

    def run(self):
        self.show_start_screen()  # Show the start screen before game loop
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
