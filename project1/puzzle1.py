import pygame
import random

# Pygame setup
pygame.init()


def solve_puzzle():
    # Set up the game window
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Ramen Puzzle")

    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    # Puzzle: Simple math problem
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    correct_answer = num1 + num2

    long_text = """The cook is putting together your ramen–you’re basically salivating–but right
    before he was about to hand you your bowl, he handed you a sheet of paper with what
    seems to be random letters put together. He strikes up an offer:
    If you can unscramble the word written on this paper, you can get this bowl of ramen for
    free. HOLY MOLY! How can you pass up on this offer?"""

    # Display question
    question_text = font.render(long_text, True, (255, 255, 255))
    answer_box = pygame.Rect(150, 200, 100, 50)
    answer_input = ""

    running = True
    puzzle_solved = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check if the answer is correct
                    if answer_input.isdigit() and int(answer_input) == correct_answer:
                        puzzle_solved = True
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    answer_input = answer_input[:-1]
                else:
                    answer_input += event.unicode

        # Fill the screen with a background color
        screen.fill((0, 0, 0))

        # Display the question
        screen.blit(question_text, (50, 50))

        # Display the input box and the user's answer
        pygame.draw.rect(screen, (255, 255, 255), answer_box, 2)
        answer_text = font.render(answer_input, True, (255, 255, 255))
        screen.blit(answer_text, (answer_box.x + 10, answer_box.y + 10))

        pygame.display.flip()
        clock.tick(30)  # Frames per second

    pygame.quit()
    return puzzle_solved
