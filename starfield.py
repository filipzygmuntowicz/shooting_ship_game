
import math
import random


class Star:

    def __init__(self, position_x, position_y, distance, angle, speed, size,
                 color):
        self.position_x = position_x
        self.position_y = position_y
        self.distance = distance
        self.size = size
        self.angle = angle
        self.speed = speed
        self._calculate_axis_speeds()
        self.color = (int(distance * color[0]),
                      int(distance * color[1]),
                      int(distance * color[2]))

    def draw(self, display):
        display.fill(self.color, (self.position_x, self.position_y,
                                  self.size, self.size))
        return

    def erase(self, display):
        display.fill((0, 0, 0), (self.position_x, self.position_y,
                                 self.size, self.size))
        return

    def move(self, elapsed_time):
        self.position_x += (self.speed_x * elapsed_time)
        self.position_y += (self.speed_y * elapsed_time)
        return

    def set_angle(self, new_angle):
        self.angle = new_angle
        self._calculate_axis_speeds()

    def set_speed(self, new_speed):
        self.speed = new_speed
        self._calculate_axis_speeds()

    def _calculate_axis_speeds(self):
        # This is a pretty slow function - performance is poor because of
        # the math. If you had a game where the starfield could only move
        # in certain directions, or at certain speeds, you might be able to
        # increase performance by precalculating the values you need, and
        # feeding them in as constants.
        self.speed_x = math.cos(self.angle / (180 / math.pi)) * self.speed
        self.speed_y = math.sin(self.angle / (180 / math.pi)) * self.speed


class Starfield:
    def __init__(self, display, rect, number_of_stars, angle,
                 speed_sequence, timer, size=1, color=(255, 255, 255)):
        self.display_surface = display
        self.display_rect = rect
        self.angle = angle
        self.fastest_star_speed = speed_sequence[0]
        self.slowest_star_speed = speed_sequence[1]
        self.brightest_color = color
        self.number_of_stars = number_of_stars
        self.timer = timer()

        # create our stars

        self.stars = []
        for index in range(number_of_stars):
            x_pos = self._random_x()
            y_pos = self._random_y()
            distance = random.random()
            speed = ((distance *
                      (self.fastest_star_speed - self.slowest_star_speed)) +
                     self.slowest_star_speed)

            my_star = Star(x_pos, y_pos, distance, angle, speed, size, color)
            self.stars.append(my_star)

    def update(self):
        self.erase()
        self.move()
        self.draw()

    def draw(self):
        for my_star in self.stars:
            my_star.draw(self.display_surface)
        return

    def erase(self):
        for my_star in self.stars:
            my_star.erase(self.display_surface)
        return

    def move(self):
        elapsed_time = self.timer.get_elapsed_time()
        for my_star in self.stars:
            my_star.move(elapsed_time)
            # Check if the star has moved off a screen edge. If so, put it
            # back on the opposite screen edge at a random position.
            if my_star.position_x <= self.display_rect.left:
                my_star.position_x = self.display_rect.right
                my_star.position_y = self._random_y()
            elif my_star.position_x >= self.display_rect.right:
                my_star.position_x = self.display_rect.left
                my_star.position_y = self._random_y()
            if my_star.position_y <= self.display_rect.top:
                my_star.position_y = self.display_rect.bottom
                my_star.position_x = self._random_x()
            elif my_star.position_y >= self.display_rect.bottom:
                my_star.position_y = self.display_rect.top
                my_star.position_x = self._random_x()
        return

    def set_angle(self, new_angle):
        self.angle = new_angle
        for star in self.stars:
            star.set_angle(new_angle)
        return

    def set_speeds(self, new_speed_sequence):
        self.fastest_star_speed = new_speed_sequence[0]
        self.slowest_star_speed = new_speed_sequence[1]
        for star in self.stars:
            new_speed = ((star.distance *
                         (self.fastest_star_speed-self.slowest_star_speed)) +
                         self.slowest_star_speed)
            star.set_speed(new_speed)
        return

    def _random_x(self):
        return float(random.randint(self.display_rect.left,
                                    self.display_rect.right))

    def _random_y(self):
        return float(random.randint(self.display_rect.top,
                                    self.display_rect.bottom))
