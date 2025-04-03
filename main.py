import pygame
import sys
import random
from button import Button
from player import Player

def ball_animation():
    global ball_speed_x, ball_speed_y, opp_score, last_touched, current_state, player2_paddle
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        player_paddle.score += 1
        ball_restart()

    if ball.right >= screen_width:
        if current_state == 'playing_ai':
            opp_score += 1
        elif current_state == 'playing_multiplayer' and player2_paddle:
            player2_paddle.score += 1
        ball_restart()

    if ball.colliderect(player_paddle.rect):
        last_touched = True
        ball_speed_x *= -1

    opponent_rect = None
    if current_state == 'playing_ai':
        opponent_rect = opp
    elif current_state == 'playing_multiplayer' and player2_paddle:
        opponent_rect = player2_paddle.rect

    if opponent_rect and ball.colliderect(opponent_rect):
        last_touched = False
        ball_speed_x *= -1


def opp_ai_animation():
    global opponent_speed
    if opp.top < ball.y:
        opp.top += opponent_speed
    if opp.bottom > ball.y:
        opp.bottom -= opponent_speed
    if opp.top <= 0:
        opp.top = 0
    if opp.bottom >= screen_height:
        opp.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y = 7 * random.choice((1, -1))
    ball_speed_x = 7 * random.choice((1, -1))


def fruit():
    global fruit_active, last_touched, opp_score, current_state, player2_paddle

    if not fruit_active:
        return

    opponent_rect = None
    if current_state == 'playing_ai':
        opponent_rect = opp
    elif current_state == 'playing_multiplayer' and player2_paddle:
        opponent_rect = player2_paddle.rect

    if fruit_rect.colliderect(ball):
        if last_touched:
            player_paddle.score += 10
            print("Player 1 got fruit bonus!")
        else:
            if current_state == 'playing_ai':
                opp_score += 10
                print("Opponent got fruit bonus!")
            elif current_state == 'playing_multiplayer' and player2_paddle:
                 player2_paddle.score += 10
                 print("Player 2 got fruit bonus!")

        fruit_respawn(fruit_rect, player_paddle, opponent_rect)


def fruit_respawn(f_rect, player1, opponent_obj):
    global fruit_active
    fruit_active = True
    opponent_rect_to_check = None
    if isinstance(opponent_obj, Player): # Check if it's Player 2
        opponent_rect_to_check = opponent_obj.rect
    elif isinstance(opponent_obj, pygame.Rect): # Check if it's the AI opp Rect
         opponent_rect_to_check = opponent_obj

    while True:
        f_width = random.randint(50, screen_width - 100)
        f_height = random.randint(50, screen_height - 100)
        f_rect.topleft = (f_width, f_height)
        f_rect.size = (40, 40)

        collides_p1 = f_rect.colliderect(player1.rect)
        collides_opp = False
        if opponent_rect_to_check:
            collides_opp = f_rect.colliderect(opponent_rect_to_check)

        if collides_p1 or collides_opp:
            continue
        break


def draw_start_menu():
    screen.fill(bg_color)
    title_text = title_font.render("Pong Game", True, light_grey)
    title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 2 - 150))
    screen.blit(title_text, title_rect)
    button_play.draw(screen)
    button_close.draw(screen)

def draw_mode_select_menu():
    screen.fill(bg_color)
    select_text = title_font.render("Select Mode", True, light_grey)
    select_rect = select_text.get_rect(center=(screen_width / 2, screen_height / 2 - 150))
    screen.blit(select_text, select_rect)
    button_vs_ai.draw(screen)
    button_multiplayer.draw(screen)
    button_back.draw(screen) # Add a back button

def start_game_common_setup(f_rect, player1):
    global opp_score
    player1.reset()
    opp_score = 0
    ball_restart()
    # Determine opponent object for fruit respawn based on state
    opponent_obj = None
    if current_state == 'playing_ai':
        opp.centery = screen_height / 2
        opponent_obj = opp
    elif current_state == 'playing_multiplayer' and player2_paddle:
        player2_paddle.reset()
        opponent_obj = player2_paddle

    if opponent_obj:
        fruit_respawn(f_rect, player1, opponent_obj)
    else: # Fallback if state is wrong somehow
         fruit_respawn(f_rect, player1, None)


def action_start_ai():
    global current_state, player2_paddle
    print("Starting AI Game!")
    current_state = 'playing_ai'
    player2_paddle = None # Ensure no player 2
    start_game_common_setup(fruit_rect, player_paddle)

def action_start_multiplayer():
    global current_state, player2_paddle
    print("Starting Multiplayer Game!")
    current_state = 'playing_multiplayer'
    # Create player 2 if it doesn't exist
    if not player2_paddle:
         player2_paddle = Player(
            x=10, # Left side
            y=screen_height / 2 - 70,
            width=10,
            height=140,
            color=GREEN, # Different color
            screen_height=screen_height,
            up_key=pygame.K_w, # WASD controls
            down_key=pygame.K_s
        )
    start_game_common_setup(fruit_rect, player_paddle)

def action_go_to_menu():
    global current_state
    current_state = 'menu'

def action_select_mode():
     global current_state
     current_state = 'mode_select'

def close_game():
    print("Closing game.")
    pygame.quit()
    sys.exit()


pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
fruit_color= (255,0,0)
GREEN = (0,225,0)
hover_GREEN =(0,150,0)
RED = (255,0,0)
hover_RED = (190,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
hover_YELLOW = (200, 200, 0)

game_font = pygame.font.Font("freesansbold.ttf", 32)
title_font = pygame.font.Font("freesansbold.ttf", 75)

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
opp = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
fruit_rect = pygame.Rect(0, 0, 40, 40)
fruit_active = False

player_paddle = Player(
    x=screen_width - 20,
    y=screen_height / 2 - 70,
    width=10,
    height=140,
    color=BLUE,
    screen_height=screen_height,
    up_key=pygame.K_UP,
    down_key=pygame.K_DOWN
)
player2_paddle = None # Initialize player 2 as None

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
opponent_speed = 7
opp_score = 0
last_touched = True

current_state = 'menu'

button_play = Button(
    x = screen_width / 2 - 75, # Centered single button
    y = screen_height / 2 + 50,
    width = 150,
    height = 50,
    text = "Play",
    font=game_font,
    button_color =GREEN,
    hover_color = hover_GREEN,
    action = action_select_mode # Goes to mode select screen
)
button_close = Button(
    x = screen_width / 2 - 75, # Centered single button
    y = screen_height / 2 + 120, # Below play
    width = 150,
    height = 50,
    text = "Quit",
    font=game_font,
    button_color = RED,
    hover_color = hover_RED,
    action = close_game
)

button_vs_ai = Button(
    x = screen_width / 2 - 150 - 20,
    y = screen_height / 2 + 50,
    width = 150,
    height = 50,
    text = "vs AI",
    font=game_font,
    button_color =BLUE,
    hover_color = light_grey,
    action = action_start_ai
)
button_multiplayer = Button(
    x = screen_width / 2 + 20,
    y = screen_height / 2 + 50,
    width = 150,
    height = 50,
    text = "Multiplayer",
    font=game_font,
    button_color = GREEN,
    hover_color = hover_GREEN,
    action = action_start_multiplayer
)
button_back = Button(
    x = screen_width / 2 - 75,
    y = screen_height / 2 + 120, # Below mode buttons
    width = 150,
    height = 50,
    text = "Back",
    font=game_font,
    button_color = YELLOW,
    hover_color = hover_YELLOW,
    action = action_go_to_menu
)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game()

        if current_state == 'menu':
            button_play.handle_event(event)
            button_close.handle_event(event)
        elif current_state == 'mode_select':
            button_vs_ai.handle_event(event)
            button_multiplayer.handle_event(event)
            button_back.handle_event(event)
        elif current_state == 'playing_ai':
            player_paddle.handle_input(event)
        elif current_state == 'playing_multiplayer':
            player_paddle.handle_input(event)
            if player2_paddle:
                player2_paddle.handle_input(event)


#CALLING THE STATES FOR THE OPPONENTS

    if current_state == 'playing_ai' or current_state == 'playing_multiplayer':
        ball_animation()
        player_paddle.move()
        if current_state == 'playing_ai':
            opp_ai_animation()
        elif current_state == 'playing_multiplayer' and player2_paddle:
            player2_paddle.move()
        fruit()


    screen.fill(bg_color)

    if current_state == 'playing_ai' or current_state == 'playing_multiplayer':
        player_paddle.draw(screen)

        opponent_score_display = 0
        if current_state == 'playing_ai':
            pygame.draw.rect(screen, light_grey, opp)
            opponent_score_display = opp_score
        elif current_state == 'playing_multiplayer' and player2_paddle:
            player2_paddle.draw(screen)
            opponent_score_display = player2_paddle.score

        if fruit_active:
            pygame.draw.ellipse(screen, fruit_color, fruit_rect)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        player_text = game_font.render(f"{player_paddle.score}", False, light_grey)
        screen.blit(player_text, (screen_width / 2 + 20, screen_height / 2 - 16))
        opp_text = game_font.render(f"{opponent_score_display}", False, light_grey)
        screen.blit(opp_text, (screen_width / 2 - opp_text.get_width() - 20, screen_height / 2 - 16))

    elif current_state == 'menu':
        draw_start_menu()
    elif current_state == 'mode_select':
        draw_mode_select_menu()


    pygame.display.flip()
    clock.tick(60)
