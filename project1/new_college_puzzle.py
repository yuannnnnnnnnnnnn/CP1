import pygame

# Initialize Pygame
pygame.init()


def display_text():
    """Displays the word scramble puzzle and handles user input."""
    # Set up the game window
    screen_width, screen_height = 600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ramen Puzzle")

    # Load and resize image
    chef_image = pygame.image.load("chef_image.png")
    chef_image = pygame.transform.scale(chef_image, (600, 600))  # Adjust size as needed
    chef_x = (screen_width - chef_image.get_width()) // 2
    chef_y = (screen_height - chef_image.get_height()) // 2

    # Define the font
    font_size = 30
    font = pygame.font.SysFont(None, font_size)
    input_font = pygame.font.SysFont(None, 40)  # Font for the input text
    clock = pygame.time.Clock()

    # Long text
    long_text = """The cook is putting together your ramen–you’re basically salivating–but right
    before he was about to hand you your bowl, he handed you a sheet of paper with what
    seems to be random letters put together. He strikes up an offer:
    If you can unscramble the word written on this paper, you can get this bowl of ramen for
    free. HOLY MOLY! How can you pass up on this offer?"""

    # Wrap the text based on screen width
    lines = wrap_text(long_text, font, screen_width - 40)  # Subtract padding from screen width

    scrambled_word = "tostuank"  # The scrambled version of "tonkatsu"
    correct_answer = "tonkatsu"  # Correct answer for the puzzle
    user_input = ""  # Input that user types
    input_active = False  # State if the input box is active or not
    message = ""  # Message to show result feedback

    running = True
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
                            message = "Correct! You get the ramen!"
                        else:
                            message = "Wrong! Try again."
                        user_input = ""  # Clear input after pressing enter
                    else:
                        user_input += event.unicode  # Add typed character to input

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Render the wrapped text
        y_offset = 20  # Starting position for the first line
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))  # Render the line in white
            screen.blit(text_surface, (20, y_offset))  # Draw the text surface to the screen
            y_offset += font.get_height()  # Space between lines dynamically adjusts with font height

        # Draw the scrambled word
        scrambled_text = font.render(f"Scrambled word: {scrambled_word}", True, (255, 255, 0))  # Yellow color
        screen.blit(scrambled_text, (screen_width // 2 - scrambled_text.get_width() // 2, y_offset + 10))

        # Draw the image onto the screen
        screen.blit(chef_image, (chef_x, chef_y))

        # Draw the input box
        input_box = pygame.Rect(50, screen_height - 65, screen_width - 100, 40)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

        # Render the user's typed text in the input box
        input_text_surface = input_font.render(user_input, True, (0, 0, 0))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))  # Position the text inside the box

        # Display feedback message
        if message:
            message_surface = font.render(message, True, (0, 255, 0) if message.startswith("Correct") else (255, 0, 0))  # Green for correct, red for wrong
            screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height - 110))

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Set the frame rate to 30 FPS

    pygame.quit()


def wrap_text(text, font, max_width):
    """Wrap text to fit within the specified width."""
    lines = []
    words = text.split(' ')  # Split text into words

    current_line = ""
    for word in words:
        # Check if adding the word exceeds the max width
        test_line = f"{current_line} {word}".strip()
        test_surface = font.render(test_line, True, (255, 255, 255))

        if test_surface.get_width() <= max_width:
            current_line = test_line  # Add word to current line
        else:
            # If the line exceeds the max width, start a new line
            lines.append(current_line)
            current_line = word

    # Add the last line if there is any remaining text
    if current_line:
        lines.append(current_line)

    return lines


# Run the display function
display_text()
