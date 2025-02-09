import pygame

# Initialize Pygame
pygame.init()

def display_text():
    """..."""
    # Set up the game window
    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ramen Puzzle")

    # Define the font size
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

    answer = "ramen"  # Correct answer for the puzzle
    user_input = ""  # Input that user types
    input_active = False  # State if the input box is active or not
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle input box active state when clicked
                if 50 <= pygame.mouse.get_pos()[0] <= screen_width - 50 and screen_height - 70 <= pygame.mouse.get_pos()[1] <= screen_height - 30:
                    input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]  # Remove last character
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower() == answer:
                            print("Correct! You get the ramen.")
                        else:
                            print("Wrong! Try again.")
                        user_input = ""  # Clear input after pressing enter
                    else:
                        user_input += event.unicode  # Add typed character to input

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Render the wrapped text
        y_offset = 50  # Starting position for the first line
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))  # Render the line in white
            screen.blit(text_surface, (20, y_offset))  # Draw the text surface to the screen
            y_offset += font.get_height()  # Space between lines dynamically adjusts with font height

        # Draw the input box
        input_box = pygame.Rect(50, screen_height - 70, screen_width - 100, 40)  # Position and size of the box
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)  # Draw the box with a white border

        # Render the user's typed text in the input box
        input_text_surface = input_font.render(user_input, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))  # Position the text inside the box

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
