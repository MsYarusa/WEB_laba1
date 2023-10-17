import pygame as pg
import random

WIDTH = 800
HEIGHT = 640
SIZE = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)

horizontal_borders = pg.sprite.Group()
vertical_borders = pg.sprite.Group()
balls = pg.sprite.Group()
all_sprites = pg.sprite.Group()

buffer = []
buff_screen = pg.Surface(SIZE)


class Ball(pg.sprite.Sprite):
    def __init__(self, radius, x, y, color):
        super().__init__(all_sprites)
        self.add(balls)
        self.radius = radius
        self.image = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color(color), (radius, radius), radius)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = pg.Rect(x, y, 2 * radius, 2 * radius)

        vx = random.randint(-5, 5)
        while not vx:
            vx = random.randint(-5, 5)

        vy = random.randint(-5, 5)
        while not vy:
            vy = random.randint(-5, 5)

        self.vx = vx
        self.vy = vy

        if x + 2 * radius + 5 > WIDTH or x - 5 < 0:
            self.kill()

        if y + 2 * radius + 5 > HEIGHT or y - 5 < 0:
            self.kill()

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pg.sprite.spritecollideany(self, horizontal_borders):
            delta_x = WIDTH // 2 - self.rect.centerx
            delta_y = HEIGHT // 2 - self.rect.centery
            dist = round((delta_x ** 2 + delta_y ** 2) ** 0.5)
            self.rect.move_ip( 3 * delta_x // dist, 3 * delta_y // dist)
            self.vy = -self.vy

        if pg.sprite.spritecollideany(self, vertical_borders):
            delta_x = WIDTH // 2 - self.rect.centerx
            delta_y = HEIGHT // 2 - self.rect.centery
            dist = round((delta_x ** 2 + delta_y ** 2) ** 0.5)
            self.rect.move_ip(3 * delta_x // dist, 3 * delta_y // dist)
            self.vx = -self.vx

        for ball in balls:
            if ball is not self and pg.sprite.collide_mask(self, ball) is not None:
                delta_x = self.rect.centerx - ball.rect.centerx
                delta_y = self.rect.centery - ball.rect.centery
                dist = round((delta_x ** 2 + delta_y ** 2) ** 0.5)

                self.rect.move_ip(delta_x // dist, delta_y // dist)
                ball.rect.move_ip(-1 * delta_x // dist, -1 * delta_y // dist)
                self.vx, ball.vx = ball.vx, self.vx
                self.vy, ball.vy = ball.vy, self.vy


class Border(pg.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


def start_game():
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption('Шарики')

    color = pg.Color(255, 0, 0)
    hsv = color.hsva

    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

    clock = pg.time.Clock()
    FPS = 60

    running = True
    while running:

        clock.tick(FPS)

        if buffer:
            for pos in buffer:
                color.hsva = ((hsv[0] + random.randint(0, 360)) % 360, hsv[1], hsv[2], hsv[3])
                Ball(20, int(pos[0]), int(pos[1]), color)
                all_sprites.update()
                buffer.remove(pos)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        all_sprites.update()
        screen.fill(WHITE)
        all_sprites.draw(screen)
        buff_screen.blit(screen, (0, 0))
        pg.display.flip()