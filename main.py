import pygame
import sys
from pygame.locals import QUIT, K_SPACE
from random import randint

# Инициализация Pygame
pygame.init()

# Скорость игры (количество кадров в секунду)
FPS = 60
# Инициализация объекта Clock для управления FPS
Frames = pygame.time.Clock()

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Цвета
BG = (70, 195, 219)


# Установка заголовка окна
pygame.display.set_caption("Flappy bird python")
# Создание поверхности экрана
screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка изображения фона
background_image = pygame.image.load("background.jpg")
# Масштабирование изображения фона до размеров экрана
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Bird:
    def __init__(self, game_instance):
        # Загрузка изображения птицы
        self.image = pygame.image.load("flappy.png")
        # Получение прямоугольника, ограничивающего изображение птицы
        self.rect = self.image.get_rect()
        # Начальная позиция птицы
        self.rect.top = SCREEN_HEIGHT / 2 - self.rect.height / 2
        self.rect.left = 20
        # Начальная скорость птицы по вертикали
        self.velocity = 1
        # Гравитация, определяющая ускорение птицы вниз
        self.gravity = 0.5
        # Угол поворота птицы
        self.angle = 0
        # Скорость изменения угла поворота птицы
        self.angle_speed = 2.5
        # Флаг подъема птицы (нажата ли клавиша пробела)
        self.rising = False
        # Ссылка на экземпляр игры
        self.game_instance = game_instance

    def draw(self, surface):
        # Отрисовка птицы с учетом поворота
        rotated_images = pygame.transform.rotate(self.image, self.angle)
        surface.blit(rotated_images, self.rect)

    def update(self):
        # Обновление позиции птицы и скорости, если игра активна
        if game.get_status():
            self.rect.move_ip(0, self.velocity)
            self.velocity += self.gravity
            # Обработка нажатия клавиши пробела
            self.key_press()
            # Управление поворотом птицы
            if self.velocity > 0:
                self.rising = False
            if self.rising and self.angle < 25:
                self.angle += self.angle_speed
            elif not self.rising and self.angle > -15:
                self.angle -= self.angle_speed * 0.5
        # Установка скорости на 0, если игра завершена
        else:
            self.velocity = 0
    def key_press(self):
        # Обработка нажатия клавиши пробела (подъем птицы)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            self.velocity = -5
            self.rising = True

    def check_collision(self, pipe):
        # Проверка столкновения птицы с трубой
        if (pipe.rect_top.left <= self.rect.right and pipe.rect_top.bottom >= self.rect.top) \
                or (pipe.rect_bottom.left <= self.rect.right and pipe.rect_bottom.top <= self.rect.bottom):
            game.end_game()

    def end_game(self):
        # Останавливаем птицу
        self.velocity = 0
        # Завершаем игру
        self.game_instance.end_game()

class Pipe:
    def __init__(self):
        # Ширина и высота трубы
        self.width = 120
        self.height = 250
        # Загрузка изображения трубы для верхней и нижней частей
        self.image_top = pygame.image.load("pipe4.png")
        self.image_top = pygame.transform.rotate(self.image_top, 180)
        self.image_top = pygame.transform.scale(self.image_top, (self.width, self.height))
        self.rect_top = self.image_top.get_rect()
        self.rect_top.top = 0
        self.rect_top.right = SCREEN_WIDTH + self.width
        # Скорость движения трубы
        self.speed = -6
        # Аналогично для нижней части трубы
        self.image_bottom = pygame.image.load("pipe4.png")
        self.image_bottom = pygame.transform.rotate(self.image_bottom, 0)
        self.image_bottom = pygame.transform.scale(self.image_bottom, (self.width, self.height))
        self.rect_bottom = self.image_bottom.get_rect()
        self.rect_bottom.bottom = SCREEN_HEIGHT
        self.rect_bottom.right = SCREEN_WIDTH + self.width
        # Флаг, указывающий, прошла ли труба игрока
        self.passed = False  # Добавляем этот флаг

    def draw(self, surface):
        # Отрисовка трубы (верхней и нижней частей)
        surface.blit(self.image_top, self.rect_top)  # Верхнее препятствие
        surface.blit(self.image_bottom, self.rect_bottom)  # Нижнее препятствие

    def update(self):
        # Обновление позиции трубы
        self.rect_top.move_ip(self.speed, 0)
        self.rect_bottom.move_ip(self.speed, 0)
        # Проверка, вышла ли труба за границу экрана
        if self.rect_top.right < 0:
            # Если да, то переустановка трубы на правый край экрана
            self.image_top = pygame.image.load("pipe4.png")
            self.image_top = pygame.transform.rotate(self.image_top, 180)
            self.image_top = pygame.transform.scale(self.image_top, (self.width, self.random_height()))
            self.rect_top = self.image_top.get_rect()
            self.rect_top.right = SCREEN_WIDTH + self.width
            # Аналогично для нижней части трубы
            self.image_bottom = pygame.image.load("pipe4.png")
            self.image_bottom = pygame.transform.rotate(self.image_bottom, 0)
            self.image_bottom = pygame.transform.scale(self.image_bottom, (self.width, self.random_height()))
            self.rect_bottom = self.image_bottom.get_rect()
            self.rect_bottom.bottom = SCREEN_HEIGHT
            self.rect_bottom.right = SCREEN_WIDTH + self.width
            # Сброс флага прохождения трубы игроком
            self.passed = False  # Сбрасываем флаг для каждой трубы

    def passed_bird(self, bird_rect):
        # Проверка, прошла ли птица трубу
        if not self.passed and self.rect_top.right < bird_rect.left:
            self.passed = True
            return True
        return False

    def random_height(self):
        # Генерация случайной высоты трубы
        return randint(100, 250)


class Game:
    def __init__(self):
        # Статус игры (активна ли игра)
        self.status = True
        self.score = 0  # Добавляем переменную для хранения счета

    def increase_score(self):
        self.score += 1  # Увеличиваем счет

    def get_score(self):
        return self.score

    def reset_score(self):
        self.score = 0  # Сбрасываем счет

    def get_status(self):
        # Получение статуса игры
        return self.status

    def end_game(self):
        # Окончание игры (установка статуса игры на "False")
        self.status = False
        self.reset_score()  # Сбрасываем счет при завершении игры

    def end_title(self, surface):
        # Отображение текста "Конец игры" по центру экрана
        text_color = (254, 255, 137)
        bg_color = (48, 58, 82)
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Конец игры", True, text_color, bg_color)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        surface.blit(text, text_rect)



# Создание объектов игры (птицы, трубы и игры)
game = Game()
bird = Bird(game)
pipe = Pipe()



# Отображение счетчика
font = pygame.font.Font(None, 36)
score_text = font.render("Score: " + str(game.get_score()), True, (255, 255, 255))
screen_surface.blit(score_text, (10, 10))


# Главный игровой цикл

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            # Обработка события закрытия окна
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game.get_status():
                # Если игра завершена и нажата клавиша "пробел", перезапускаем игру
                bird.rect.top = SCREEN_HEIGHT / 2 - bird.rect.height / 2
                bird.rect.left = 20
                pipe.rect_top.right = SCREEN_WIDTH + pipe.width
                pipe.rect_bottom.right = SCREEN_WIDTH + pipe.width
                # Сброс флага прохождения трубы игроком
                pipe.passed = False
                game.status = True
                game.reset_score()  # Сбрасываем счет при начале новой игры



    # Обновление позиции птицы и трубы (если игра активна)
    bird.update()
    if game.get_status():
        pipe.update()
        bird.check_collision(pipe)
        # Проверка прохождения трубы и увеличение счетчика
        if pipe.passed_bird(bird.rect):
            game.increase_score()

    # Отрисовка игровых объектов на экране
    # Отображение фонового изображения
    screen_surface.blit(background_image, (0, 0))

    #screen_surface.fill(BG)
    bird.draw(screen_surface)
    pipe.draw(screen_surface)
    if not game.get_status():
        # Если игра окончена, отображение текста "Конец игры"
        game.end_title(screen_surface)

    # Отображение счетчика
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(game.get_score()), True, (255, 255, 255))
    screen_surface.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.update()
    # Управление FPS игры
    Frames.tick(FPS)
