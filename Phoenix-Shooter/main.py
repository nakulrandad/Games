import os
import sys
import pygame
import random

pygame.init()

FPS = 50
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phoenix Shooter")
asset_file_loc = os.path.join(os.path.dirname(__file__), "assets")

# Load images
RED_SPACE_SHIP = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_ship_red_small.png")
)
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_ship_green_small.png")
)
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_ship_blue_small.png")
)

# Player image
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_ship_yellow.png")
)
ORANGE_SPACE_SHIP = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_ship_orange.png")
)

# Lasers
RED_LASER = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_laser_red.png")
)
GREEN_LASER = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_laser_green.png")
)
BLUE_LASER = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_laser_blue.png")
)
YELLOW_LASER = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_laser_yellow.png")
)
ORANGE_LASER = pygame.image.load(
    os.path.join(asset_file_loc, "pixel_laser_orange.png")
)

# Powerups
HEART = pygame.transform.scale(
    pygame.image.load(os.path.join(asset_file_loc, "heart_trans.png")),
    (70, 70),
)
LIFE = pygame.transform.scale(
    pygame.image.load(os.path.join(asset_file_loc, "life_trans.png")), (45, 45)
)
ELECTRIC = pygame.transform.scale(
    pygame.image.load(os.path.join(asset_file_loc, "electric_trans.png")),
    (60, 60),
)

# Background
MAIN_BG = pygame.transform.scale(
    pygame.image.load(os.path.join(asset_file_loc, "bg_2.png")),
    (WIDTH, HEIGHT),
)
BG = []
BG.append(
    pygame.transform.scale(
        pygame.image.load(
            os.path.join(asset_file_loc, "background-black.png")
        ),
        (WIDTH, HEIGHT),
    )
)
BG.append(
    pygame.transform.scale(
        pygame.image.load(os.path.join(asset_file_loc, "bg.png")),
        (WIDTH, HEIGHT),
    )
)
BG.append(
    pygame.transform.scale(
        pygame.image.load(os.path.join(asset_file_loc, "bg_3_edit.png")),
        (WIDTH, HEIGHT),
    )
)


def play_music(location):
    pygame.mixer.music.load(os.path.join(asset_file_loc, location))
    pygame.mixer.music.play()


class Power:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y < -45 or self.y > height

    def collision(self, obj):
        return collide(self, obj)


class Powerup(Power):
    POWER_IMGS = {"heart": HEART, "life": LIFE, "electric": ELECTRIC}

    def __init__(self, x, y, kind):
        super().__init__(x, y, self.POWER_IMGS[kind])
        self.kind = kind

    def increase_life(self, obj):
        obj.lives += 1

    def increase_health(self, obj):
        obj.health = obj.max_health

    def increase_speed(self, obj):
        obj.high_speed_time += 20 * FPS
        obj.COOLDOWN = obj.ELECRIC_COOLDOWN


class Laser(Power):
    pass


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.COOLDOWN = FPS / 2

    def draw(self, window):
        for laser in self.lasers:
            laser.draw(window)
        window.blit(self.ship_img, (self.x, self.y))

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    player_num = 1

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        if Player.player_num % 2 == 1:
            self.ship_img = YELLOW_SPACE_SHIP
            self.laser_img = YELLOW_LASER
        else:
            self.ship_img = ORANGE_SPACE_SHIP
            self.laser_img = ORANGE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.vel = 10
        self.lives = 3
        self.score = 0
        self.COOLDOWN = FPS / 4  # Overwrite
        self.ELECRIC_COOLDOWN = FPS / 6
        self.high_speed_time = 0
        if Player.player_num % 2 == 1:  # Modulo max number of players
            self.player_id = 1
        else:
            self.player_id = 2
        Player.add_player()

    @classmethod
    def add_player(cls):
        cls.player_num += 1

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            if self.high_speed_time == 0:
                laser.move(vel)
                self.COOLDOWN = FPS / 4
            elif self.high_speed_time > 0:
                laser.move(vel * 2)  # Powerup highspeed laser

            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score += 10
                        play_music("music/enemy_explosion.mp3")
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def add_score(self, points=10):
        self.score += points

    def healthbar(self, window):
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width(),
                10,
            ),
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width() * (self.health / self.max_health),
                10,
            ),
        )


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    bgY = 0
    bgY2 = HEIGHT

    run = True
    level = 0
    main_font = pygame.font.SysFont("comicsans", 35)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    powerups = []
    players = []
    dead_players = []
    wave_length = 5

    enemy_vel = 1
    powerup_vel = 2
    laser_vel = 3

    player1 = Player(WIDTH / 2 - WIDTH / 4, HEIGHT - 150)
    players.append(player1)

    if num_of_players == 2:
        player2 = Player(WIDTH / 2 + WIDTH / 4, HEIGHT - 150)
        players.append(player2)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG[((level - 1) // 3) % 3], (0, bgY))
        WIN.blit(BG[((level - 1) // 3) % 3], (0, bgY2))

        # text
        levels_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        for powerup in powerups:
            powerup.draw(WIN)

        for player in players:
            player.draw(WIN)

        for player in players + dead_players:
            score_label = main_font.render(
                f"Score: {player.score}", 1, (255, 255, 255)
            )
            WIN.blit(
                score_label,
                (
                    WIDTH / 2 - score_label.get_width() / 2,
                    10 + (player.player_id - 1) * 28,
                ),
            )
            lives_label = main_font.render(
                f"Player {player.player_id} - Lives: {player.lives}",
                1,
                (255, 255, 255),
            )
            WIN.blit(lives_label, (10, 10 + (player.player_id - 1) * 28))

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(
                lost_label,
                (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2),
            )

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        bgY += 0.8
        bgY2 += 0.8
        if bgY > HEIGHT:
            bgY = -HEIGHT
            # print("turning 1")
        if bgY2 > HEIGHT:
            bgY2 = -HEIGHT
            # print("turning 2")

        players_health = 0
        total_lives = 0
        for player in players:
            players_health += player.health
            total_lives += player.lives

        for player in players:
            if player.health <= 0:
                if player.lives > 0:
                    player.lives -= 1
                    player.health = player.max_health
                else:
                    play_music("music/player_explosion.mp3")
                    dead_players.append(player)
                    players.remove(player)

        if total_lives <= 0 and players_health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            play_music("music/level_up.mp3")

            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-HEIGHT * 2, -100),
                    random.choice(["red", "blue", "green"]),
                )
                enemies.append(enemy)

            laser_vel += 1
            wave_length += 5

        for player in players:
            if player.high_speed_time > 0:
                player.vel = 20
                player.high_speed_time -= 1
            elif player.high_speed_time == 0:
                player.vel = 10
            else:
                player.high_speed_time = 0

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False

        keys = pygame.key.get_pressed()
        is_auto_shoot = False

        if keys[pygame.K_a] and player1.x - player1.vel > 0:  # left
            player1.x -= player1.vel
        if (
            keys[pygame.K_d]
            and player1.x + player1.vel + player1.get_width() < WIDTH
        ):  # right
            player1.x += player1.vel
        if keys[pygame.K_w] and player1.y - player1.vel > 0:  # up
            player1.y -= player1.vel
        if (
            keys[pygame.K_s]
            and player1.y + player1.vel + player1.get_height() + 15 < HEIGHT
        ):  # down
            player1.y += player1.vel
        if keys[pygame.K_SPACE] or is_auto_shoot:
            player1.shoot()
            # play_music("music/laser_swoosh_cut.mp3")

        keys = pygame.key.get_pressed()

        if num_of_players == 2:
            if keys[pygame.K_LEFT] and player2.x - player2.vel > 0:  # left
                player2.x -= player2.vel
            if (
                keys[pygame.K_RIGHT]
                and player2.x + player2.vel + player2.get_width() < WIDTH
            ):  # right
                player2.x += player2.vel
            if keys[pygame.K_UP] and player2.y - player2.vel > 0:  # up
                player2.y -= player2.vel
            if (
                keys[pygame.K_DOWN]
                and player2.y + player2.vel + player2.get_height() + 15
                < HEIGHT
            ):  # down
                player2.y += player2.vel
            if keys[pygame.K_KP0] or is_auto_shoot:
                player2.shoot()
                # play_music("music/laser_swoosh_cut.mp3")

        if random.randrange(0, 80 * FPS) == 5:
            powerup1 = Powerup(
                random.randrange(30, WIDTH - 60),
                random.randrange(-HEIGHT, -50),
                "life",
            )
            powerups.append(powerup1)

        if random.randrange(0, 60 * FPS) == 3:
            powerup1 = Powerup(
                random.randrange(30, WIDTH - 60),
                random.randrange(-HEIGHT, -50),
                "heart",
            )
            powerups.append(powerup1)

        if random.randrange(0, 60 * FPS) == 7:
            powerup1 = Powerup(
                random.randrange(30, WIDTH - 60),
                random.randrange(-HEIGHT, -50),
                "electric",
            )
            powerups.append(powerup1)

        for powerup in powerups:
            powerup.move(powerup_vel)

            for player in players:
                if collide(powerup, player):
                    play_music("music/small_tick.mp3")
                    if powerup.kind == "heart":
                        powerup.increase_health(player)
                    if powerup.kind == "life":
                        powerup.increase_life(player)
                    if powerup.kind == "electric":
                        powerup.increase_speed(player)
                    powerups.remove(powerup)

        for player in players:
            for enemy in enemies[:]:
                enemy.move(enemy_vel / len(players))
                enemy.move_lasers(laser_vel / len(players), player)

                if random.randrange(0, 3 * FPS / len(players)) == 1:
                    enemy.shoot()

                if collide(enemy, player):
                    player.health -= 10
                    enemies.remove(enemy)
                    play_music("music/enemy_explosion.mp3")
                    player.add_score(10)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    for i in players:
                        i.health -= 50
                    enemies.remove(enemy)

            player.move_lasers(-laser_vel, enemies)


def main_menu():
    global num_of_players
    title_font = pygame.font.SysFont("comicsans", 60)
    run = True
    while run:
        WIN.blit(MAIN_BG, (0, 0))
        title_label = title_font.render(
            "Press 1 for one player and 2 for two...", 1, (255, 255, 255)
        )
        WIN.blit(
            title_label,
            (
                int((WIDTH - title_label.get_width()) / 2),
                int(350 / 750 * HEIGHT),
            ),
        )
        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                sys.exit()
            if keys[pygame.K_1]:
                num_of_players = 1
                play_music("music/game_begin.mp3")  # Play opening music
                pygame.time.delay(2000)
                main()
            if keys[pygame.K_2]:
                num_of_players = 2
                play_music("music/game_begin.mp3")  # Play opening music
                pygame.time.delay(2000)
                main()
    sys.exit()


main_menu()
