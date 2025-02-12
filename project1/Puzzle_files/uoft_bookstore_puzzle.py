import pygame

pygame.init()
pygame.font.init()


def display_puzzle40():
    """Displays the word scramble puzzle and handles user input."""
    # Set up the game window
    screen_width, screen_height = 400, 550
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sum Puzzle")

    # Load and resize image
    chef_image = pygame.image.load("Images/vending_machine.png")
    chef_image = pygame.transform.scale(chef_image, (400, 550))  # Adjust size as needed
    chef_x = (screen_width - chef_image.get_width()) // 2
    chef_y = (screen_height - chef_image.get_height()) // 2

    # Define the font
    font_size = 30
    font = pygame.font.SysFont(None, font_size)
    input_font = pygame.font.SysFont(None, 40)  # Font for the input text
    clock = pygame.time.Clock()

    correct_answer = "21"  # Correct answer for the puzzle
    user_input = ""  # Input that user types
    input_active = False  # State if the input box is active or not
    message = ""  # Message to show result feedback

    running = True
    success = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if input box is clicked
                if 50 <= pygame.mouse.get_pos()[0] <= screen_width - 50 and screen_height - 70 <= pygame.mouse.get_pos()[1] <= screen_height - 30:
                    input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]  # Remove last character
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower() == correct_answer:
                            message = "Correct! You get the Lip Gloss!"
                            success = True
                            running = False
                        else:
                            message = "Wrong! Try again."
                            success = False
                        user_input = ""  # Clear input after pressing enter
                    else:
                        user_input += event.unicode  # Add typed character to input

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the image onto the screen
        screen.blit(chef_image, (chef_x, chef_y))

        # Draw the input box
        input_box = pygame.Rect(50, screen_height - 65, screen_width - 100, 40)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

        # Render the user's typed text in the input box
        input_text_surface = input_font.render(user_input, True, (0, 0, 0))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))  # Position the text inside the box

        # Display feedback message
        if message:
            message_surface = font.render(message, True, (0, 255, 0) if message.startswith("Correct") else (255, 0, 0))  # Green for correct, red for wrong
            screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height - 110))

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Set the frame rate to 30 FPS

    pygame.display.quit()  # ✅ Only closes the window
    return success
