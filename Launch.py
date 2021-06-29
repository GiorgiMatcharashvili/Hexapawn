import json
import pygame
import time
from random import choice
from random import random

########################################################################################################################
##################################################### Constants ########################################################
########################################################################################################################
BACKGROUND_COLOR = (255,255,255)
BLACK = (0, 0, 0)

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
SELECTED_BLUE = (2,180,255)
SELECTED_RED = (255,180,2)

########################################################################################################################
##################################################### Variables ########################################################
########################################################################################################################

coordinates_into_color = {}
is_selected = False

########################################################################################################################
################################################# Functions for player #################################################
########################################################################################################################

def can_it_kill(current,future):
    if current[1] != 0 and current[1]-1 == future[1]:
        if current[0] == 0 and current[0]+1==future[0]:return True
        elif current[0] == 1 and current[0] != future[0]:return True
        elif current[0] == 2 and current[0]-1==future[0]:return True
        else:return False
    else:return False

def interact(coordinates):
    global is_selected

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

########################################################################################################################
########################################################## AI ##########################################################
########################################################################################################################

class AI:
    def __init__(self):
        self.move = 0
        self.get_moves()
        self.moves_which_i_did = {}

    def get_moves(self):
        with open("moves.json",) as f:
            self.moves = json.load(f)

    def set_moves(self):
        with open('moves.json', 'w') as f:
            json.dump(self.moves, f, indent=4, separators=None)

    def play(self):
        self.move += 2
        possible_moves= self.record_or_not()[1]
        my_id = self.record_or_not()[0]

        move = choice(possible_moves)

        self.make_move(move, my_id)

    def get_computer_pawns(self):
        send_list = []
        for coordinates in coordinates_into_color:
            if coordinates_into_color[coordinates] == RED:
                send_list.append(coordinates)

        return send_list

    def get_player_pawns(self):
        send_list = []
        for coordinates in coordinates_into_color:
            if coordinates_into_color[coordinates] == BLUE:
                send_list.append(coordinates)

        return send_list

    def generate_possible_moves(self):
        send_list = []

        for c in self.get_computer_pawns():
            # Check if it can move forward
            if coordinates_into_color[c[0],c[1]+1] == BACKGROUND_COLOR:
                send_list.append([c,(c[0],c[1]+1)])

            # Check for kills
            if c[0] == 0 and coordinates_into_color[c[0]+1,c[1]+1] == BLUE:
                send_list.append([c, (c[0]+1,c[1]+1)])
            if c[0] == 1 and coordinates_into_color[c[0]+1,c[1]+1] == BLUE:
                send_list.append([c, (c[0]+1, c[1]+1)])
            if c[0] == 1 and coordinates_into_color[c[0]-1,c[1]+1] == BLUE:
                send_list.append([c, (c[0]-1,c[1]+1)])
            if c[0] == 2 and coordinates_into_color[c[0]-1,c[1]+1] == BLUE:
                send_list.append([c, (c[0]-1,c[1]+1)])
        return send_list

    def generate_id(self, json):
        id = ""
        id += str(json["move"])

        for cpawn in json["computer's pawns"]:
            for each in cpawn:
                id += str(each)

        for ppawn in json["player's pawns"]:
            for each in ppawn:
                id += str(each)

        return id

    def record_or_not(self):
        send_json = {
            "move" : self.move,
            "computer's pawns": self.get_computer_pawns(),
            "player's pawns":self.get_player_pawns(),
            "possible moves":self.generate_possible_moves()
        }

        self.get_moves()

        new_id = self.generate_id(send_json)

        self.moves_which_i_did = {}

        if not new_id in self.moves.keys():
            self.moves[new_id] = send_json

            with open('moves.json', 'w') as f:
                json.dump(self.moves, f, indent=4,separators=None)
            self.moves_which_i_did[new_id] = []

            return (new_id , send_json["possible moves"])
        else:
            self.moves_which_i_did[new_id] = []
            return (new_id, self.moves[new_id]["possible moves"])

    def make_move(self,move, my_id):
        current = (move[0][0],move[0][1])
        future = (move[1][0], move[1][1])

        color_box(screen,current,SELECTED_RED)
        time.sleep(random())
        color_box(screen, current, BACKGROUND_COLOR)
        color_box(screen,future, RED)

        self.moves_which_i_did[my_id].append(move)

    def lost(self):
        # Punish
        self.get_moves()

        for move_id in self.moves_which_i_did:
            move = self.moves_which_i_did[move_id][0]
            move = [[move[0][0],move[0][1]],[move[1][0],move[1][1]]]

            self.moves[move_id]['possible moves'].remove(move)

        self.set_moves()

    def win(self):
        # Reward
        self.get_moves()

        for move_id in self.moves_which_i_did:
            move = self.moves_which_i_did[move_id][0]
            move = [[move[0][0], move[0][1]], [move[1][0], move[1][1]]]

            self.moves[move_id]['possible moves'].append(move)

        self.set_moves()

########################################################################################################################
################################################## Functions for game ##################################################
########################################################################################################################

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
            result.clear()
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
            result.clear()
            return "Red Wins"
    result.clear()

def change_text(txt,color):
    if "Wins" in txt:
        font = pygame.font.Font('freesansbold.ttf', 40)
    else:
        font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(txt, True, color, BACKGROUND_COLOR)

    textRect = text.get_rect()
    textRect.center = (300, 50)
    screen.blit(text, textRect)
    pygame.display.flip()

def show_coordinates():
    font = pygame.font.Font('freesansbold.ttf', 40)
    for x in range(0,3):
        for y in range(0,3):
            text = font.render(str(x)+","+str(y), True, BLACK, BACKGROUND_COLOR)
            textRect = text.get_rect()
            real_x = 150 + (150 * x)
            real_y = 150 + (150 * y)
            textRect.center = (real_x, real_y)
            screen.blit(text, textRect)
            pygame.display.flip()


########################################################################################################################
####################################################### Flow ###########################################################
########################################################################################################################

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
    computer = AI()

    while running:
        #show_coordinates()
        events = pygame.event.get()
        if plays == BLUE:
            change_text("Blue's turn to play!",BLACK)
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
                            is_moved = interact((row,column))
                            if is_moved:
                                result = check(plays)
                                if result != None:
                                    if "Blue" in result:
                                        change_text(f"     {result}     ",GREEN)
                                        computer.lost()
                                    elif "Red" in result:
                                        change_text(f"     {result}     ", RED)
                                        computer.win()
                                    time.sleep(1)
                                    running = False
                                else:
                                    plays = RED

            else:continue

        if plays == RED:
            change_text(" Red's turn to play!", BLACK)
            time.sleep(0.2)
            computer.play()
            time.sleep(random())
            result = check(plays)
            if result != None:
                if "Blue" in result:
                    change_text(f"     {result}     ", GREEN)
                    computer.lost()
                elif "Red" in result:
                    change_text(f"     {result}     ", RED)
                    computer.win()
                time.sleep(1)
                running = False
            else:plays = BLUE

main()
