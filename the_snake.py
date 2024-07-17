import pygame as pg
from random import choice


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (10, 10, 10)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (250, 0, 0)

# Цвет дыни
MELON_COLOR = (255, 255, 0)

# Цвет змейки
SNAKE_COLOR = (0, 150, 0)

# Скорость движения змейки:
SPEED = 19

# Центр экрана
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Все доступные ячейки
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))


# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')
# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Родительский класс для Яблока и Змейки."""

    def __init__(self, color=None, border_color=BORDER_COLOR):
        self.position = SCREEN_CENTER
        self.body_color = color
        self.border_color = border_color

    def draw(self):
        """Шаблон для отрисовки элементов."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


class RandomPozitionMixin():
    """Миксин для игровых объектов."""

    def randomize_position(self, occupied_positions=SCREEN_CENTER):
        """Выбирает рандомную позицию для съедобных объектов"""
        if not isinstance(occupied_positions, set):
            occupied_positions = set(occupied_positions)
        self.position = choice(tuple(ALL_CELLS - occupied_positions))


class Apple(GameObject, RandomPozitionMixin):
    """Дочерний класс игрового объекта - Яблоко."""

    def __init__(self, color=APPLE_COLOR, border_color=BORDER_COLOR):
        super().__init__(color, border_color)
        self.randomize_position()


class Melon(GameObject, RandomPozitionMixin):
    """Дочерний класс игрового объекта - Дыня."""

    def __init__(self, color=MELON_COLOR, border_color=BORDER_COLOR):
        super().__init__(color, border_color)
        self.randomize_position()


class Snake(GameObject):
    """Дочерний класс игрового объекта - Змейка."""

    def __init__(self, color=SNAKE_COLOR, border_color=BORDER_COLOR):
        super().__init__(color, border_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки в зависимости от направления."""
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)

    def draw(self):
        """Отрисовывам Змейку."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, self.border_color, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, self.border_color, head_rect, 1)

    def get_head_position(self):
        """Получаем позицию головы Змейки."""
        return self.positions[0]

    def reset(self):
        """
        Сбрасываем Змейку на начальное состояние после столкновения с собой
        или другого события, требующего перезапуска змейки.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажаите клавиш и выход из игры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Запускаем игру."""
    pg.init()
    apple = Apple()
    melon = Melon()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(set(
                snake.positions).union({melon.position}))
        elif snake.get_head_position() == melon.position:
            snake.length += 2
            melon.randomize_position(set(
                snake.positions).union({apple.position}))

        if len(snake.positions) > snake.length:
            snake.positions.pop()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка объектов
        apple.draw()
        melon.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
