"""Puzzle file related to friend's aparmtnet location"""

import pygame

pygame.init()
pygame.font.init()


def display_puzzle60():
    """Displays the word scramble puzzle and handles user input."""
    screen_width, screen_height = 400, 550
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Math Puzzle")

    chef_image = pygame.image.load("Images/apt_puzzle.png")
    chef_image = pygame.transform.scale(chef_image, (400, 550))
    chef_x = (screen_width - chef_image.get_width()) // 2
    chef_y = (screen_height - chef_image.get_height()) // 2

    font_size = 30
    if not pygame.font.get_init():
        pygame.font.init()

    font = pygame.font.SysFont(None, font_size)
    input_font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    correct_answer = "120"
    user_input = ""
    input_active = False
    message = ""

    running = True
    success = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 50 <= pygame.mouse.get_pos()[0] <= screen_width - 50 and screen_height - 70 <= pygame.mouse.get_pos()[1] <= screen_height - 30:
                    input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower() == correct_answer:
                            message = "Correct! You get the Lucky Mug!"
                            success = True
                            running = False
                        else:
                            message = "Wrong! Try again."
                            success = False
                        user_input = ""
                    else:
                        user_input += event.unicode

        screen.fill((0, 0, 0))

        screen.blit(chef_image, (chef_x, chef_y))

        input_box = pygame.Rect(50, screen_height - 65, screen_width - 100, 40)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        input_text_surface = input_font.render(user_input, True, (0, 0, 0))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))

        # Display feedback message
        if message:
            message_surface = font.render(message, True, (0, 255, 0) if message.startswith("Correct") else (255, 0, 0))
            screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height - 110))

        pygame.display.flip()
        clock.tick(30)

    pygame.display.quit()
    return success
