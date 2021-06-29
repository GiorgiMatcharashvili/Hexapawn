import pygame
import time

BACKGROUND_COLOR = (255,255,255)
BLACK = (0, 0, 0)

RED = (255,0,0)
BLUE = (0,0,255)
SELECTED_BLUE = (2,180,255)

coordinates_into_color = {}
is_selected = False

def createDisplay(size,name):
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption(name)

    screen.fill(BACKGROUND_COLOR)

    pygame.display.flip()

    return screen

def drawWindow(w, h):
    screen = createDisplay((w+150,h+150),"Hexapawn")

    # Draw horizontal lines
    for x in range(75,550,150):pygame.draw.line(screen, BLACK, (x,75), (x,525), 2)

    # Draw vertical lines
    for y in range(75,550,150):pygame.draw.line(screen, BLACK, (75, y), (525, y), 2)


    pygame.display.flip()

    return screen

def color_box(screen, coordinates,color):
    x = coordinates[0]
    y = coordinates[1]

    real_x = (75 + (x * 150)) + 2
    real_y = (75 + (y * 150)) + 2

    pygame.draw.rect(screen, color, pygame.Rect(real_x, real_y, 148, 148))

    pygame.display.flip()

    coordinates_into_color[coordinates] = color

def can_it_kill(current,future):
    if current[1] != 0 and current[1]-1 == future[1]:
        if current[0] == 0 and current[0]+1==future[0]:return True
        elif current[0] == 1 and current[0] != future[0]:return True
        elif current[0] == 2 and current[0]-1==future[0]:return True
        else:return False
    else:return False

def interact(coordinates):
    global is_selected, plays

    current_color = coordinates_into_color[coordinates]

    if is_selected == False:
        # Select
        if BLUE == current_color:
            color_box(screen,coordinates,SELECTED_BLUE)
            is_selected = coordinates
            return False
    else:
        # Unselect
        if SELECTED_BLUE == current_color:
            color_box(screen, coordinates, BLUE)
            is_selected = False
            return False

        # Select other one
        elif BLUE == current_color:
            color_box(screen, is_selected, BLUE)
            color_box(screen, coordinates, SELECTED_BLUE)
            is_selected = coordinates
            return False

        # Move to the empty space
        elif BACKGROUND_COLOR == current_color and is_selected[1]-1==coordinates[1] and is_selected[0]==coordinates[0]:
            color_box(screen, is_selected, BACKGROUND_COLOR)
            color_box(screen, coordinates, BLUE)
            is_selected = False
            return True

        # Kill opponent's pawn
        elif RED == current_color and can_it_kill(is_selected,coordinates):
            color_box(screen, is_selected, BACKGROUND_COLOR)
            color_box(screen, coordinates, BLUE)
            is_selected = False
            return True

def check(player):
    # Check if pawn get to the other side
    for blue in [(0,0),(1,0),(2,0)]:
        if coordinates_into_color[blue] == BLUE:
            return "Blue Wins"

    for red in [(0,2),(1,2),(2,2)]:
        if coordinates_into_color[red] == RED:
            return "Red Wins"

    # Check if all pawn dead
    game_colors =coordinates_into_color.values()
    if not RED in game_colors:
        return "Blue Wins"
    elif not BLUE in game_colors:
        return "Red Wins"

    result = set()
    # Check if opponent is left without move
    if player == BLUE:
        for coordinates in coordinates_into_color:
            if coordinates_into_color[coordinates] == RED:
                # check place in front of opponent's pawn
                if coordinates_into_color[(coordinates[0],coordinates[1]+1)] != BACKGROUND_COLOR:
                    # check kill places for player's pawns
                    if coordinates[0] == 0 and coordinates_into_color[(coordinates[0]+1,coordinates[1]+1)] != BLUE:
                        result.add(False)
                    elif (coordinates[0] == 1 and
                        coordinates_into_color[(coordinates[0]+1,coordinates[1]+1)] != BLUE and
                        coordinates_into_color[(coordinates[0]-1,coordinates[1]+1)] != BLUE):result.add(False)
                    elif coordinates[0] == 2 and coordinates_into_color[(coordinates[0]-1,coordinates[1]+1)] != BLUE:
                        result.add(False)
                    else: result.add(True)

                else: result.add(True)
        if not True in result:
            return "Blue Wins"
    elif player == RED:
        for coordinates in coordinates_into_color:
            if coordinates_into_color[coordinates] == BLUE:
                # check place in front of opponent's pawn
                if coordinates_into_color[(coordinates[0], coordinates[1] - 1)] != BACKGROUND_COLOR:
                    # check kill places for player's pawns
                    if coordinates[0] == 0 and coordinates_into_color[(coordinates[0]+1,coordinates[1]-1)] != RED:
                        result.add(False)
                    elif (coordinates[0] == 1 and
                        coordinates_into_color[(coordinates[0]+1,coordinates[1]-1)] != RED and
                        coordinates_into_color[(coordinates[0]-1,coordinates[1]-1)] != RED):result.add(False)
                    elif coordinates[0] == 2 and coordinates_into_color[(coordinates[0]-1,coordinates[1]-1)] != RED:
                        result.add(False)
                    else: result.add(True)

                else: result.add(True)
        if not True in result:
            return "RED Wins"

def change_text(txt,color):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(txt, True, color, BACKGROUND_COLOR)

    textRect = text.get_rect()
    if "Wins" in txt:
        textRect = (textRect[0],textRect[1],textRect[2],50)
    textRect.center = (300, 50)
    screen.blit(text, textRect)
    pygame.display.flip()

pygame.init()

screen = drawWindow(450, 450)

# Make board
color_box(screen,(0,0),RED)
color_box(screen,(1,0),RED)
color_box(screen,(2,0),RED)

color_box(screen,(0,1),BACKGROUND_COLOR)
color_box(screen,(1,1),BACKGROUND_COLOR)
color_box(screen,(2,1),BACKGROUND_COLOR)

color_box(screen,(0,2),BLUE)
color_box(screen,(1,2),BLUE)
color_box(screen,(2,2),BLUE)


def main():
    running = True
    plays = BLUE
    is_moved = None

    while running:
        change_text("Blue's turn to play",BLACK)

        events = pygame.event.get()
        if events != []:
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    row = None
                    column = None

                    # detect row
                    if x in range(75,225):row = 0
                    elif x in range(225,375):row = 1
                    elif x in range(375, 525):row = 2

                    # detect column
                    if y in range(75,225):column = 0
                    elif y in range(225,375):column = 1
                    elif y in range(375, 525):column = 2

                    if row is not None and column is not None:
                        if plays == BLUE:
                            is_moved = interact((row,column))
                        else: is_moved = None

        result = check(plays)
        if result is not None:
            running = False
            change_text(f"        {result}        ", (0,255,0))
            time.sleep(1)
        else:
            if is_moved is not None and is_moved == True:
                if plays == BLUE:plays= RED
                elif plays == RED:plays= BLUE
                is_moved = None

        if plays == RED:
            change_text(" Red's turn to play", BLACK)

            print("AI played")
            plays = BLUE
main()