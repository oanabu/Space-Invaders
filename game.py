import math
import random
import turtle


class Screen(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self)

        # create screen
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.title("Space Invaders")
        self.screen.bgpic("img/background.png")

        # create border
        self.speed(0)
        self.color("white")
        self.penup()
        self.setposition(-300, -300)
        self.pendown()
        self.pensize(3)

        # draw border
        for side in range(4):
            self.fd(600)
            self.lt(90)
        self.hideturtle()


class Player(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self)

        # create player
        self.penup()
        self.color("red")
        self.screen.register_shape("img/player_mo.gif")
        self.shape("img/player_mo.gif")
        self.speed(0)
        self.setposition(0, -255)
        self.setheading(90)
        self.player_speed = 15

    # move player left and right
    def move_left(self):
        x = self.xcor()
        x -= self.player_speed
        if x < -280:
            x = -280
        self.setx(x)

    def move_right(self):
        x = self.xcor()
        x += self.player_speed
        if x > 280:
            x = 280
        self.setx(x)

    def binding(self):
        self.screen.listen()
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")


class Enemy(turtle.Turtle):

    def __init__(self):
        turtle.Turtle.__init__(self)

        self.number_of_enemies = 5
        self.enemies = []
        self.enemy_speed = 2

        # add enemies to the list
        for i in range(self.number_of_enemies):
            self.enemies.append(turtle.Turtle())

        for enemy in self.enemies:
            # create enemy
            enemy.color("blue")
            enemy.screen.register_shape("img/invader_mo.gif")
            enemy.shape("img/invader_mo.gif")
            enemy.penup()
            enemy.speed(0)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)


class Weapon(Player):

    def __init__(self):
        turtle.Turtle.__init__(self)

        # create the bullet
        self.color("yellow")
        self.shape("triangle")
        self.penup()
        self.speed(0)
        self.setheading(90)
        self.shapesize(0.5, 0.5)
        self.hideturtle()
        self.bullet_speed = 20
        self.bullet_state = "ready"

    # make the bullet appear above the player
    def fire_bullet(self):
        if self.bullet_state == "ready":
            self.bullet_state = "fire"
            x = player.xcor()
            y = player.ycor() + 10
            self.setposition(x, y)
            self.showturtle()

    def is_collision(self, t1, t2):
        distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
        if distance < 15:
            return True
        else:
            return False

    def binding(self):
        self.screen.onkey(self.fire_bullet, "space")


class Game(Enemy, Weapon, Player):

    def __init__(self):
        turtle.Turtle.__init__(self)

        # create the game score
        self.score = 0
        self.score_pen = turtle.Turtle()
        self.score_string = "Score: %s" % self.score
        self.score_pen.speed(0)
        self.score_pen.color("white")
        self.score_pen.penup()
        self.score_pen.setposition(-290, 280)
        self.score_pen.write(self.score_string, False, align="left", font=("Arial", 14, "normal"))
        self.score_pen.hideturtle()

    def run(self):

        while True:

            for e in enemy.enemies:
                # move the enemy
                x = e.xcor()
                x += enemy.enemy_speed
                e.setx(x)

                # move the enemies back and down
                if e.xcor() > 280:
                    for i in enemy.enemies:
                        y = i.ycor()
                        y -= 40
                        i.sety(y)
                    enemy.enemy_speed *= -1

                if e.xcor() < -280:
                    for i in enemy.enemies:
                        y = i.ycor()
                        y -= 40
                        i.sety(y)
                    enemy.enemy_speed *= -1

                if e.ycor() < -280:
                    e.hideturtle()

                # check for a collision between the bullet and the enemy
                if weapon.is_collision(weapon, e):
                    # reset the bullet
                    weapon.hideturtle()
                    weapon.bullet_state = "ready"
                    weapon.setposition(0, -400)
                    # reset the enemy
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    # update the score
                    self.score += 10
                    self.score_string = "Score: %s" % self.score
                    self.score_pen.clear()
                    self.score_pen.write(self.score_string, False, align="left", font=("Arial", 14, "normal"))

                # check if the enemy hits the player
                if weapon.is_collision(player, e):
                    player.hideturtle()
                    e.hideturtle()
                    print("Game Over")
                    break

            y = weapon.ycor()
            y += weapon.bullet_speed
            weapon.sety(y)

            # check if the bullet has gone to the top
            if weapon.ycor() > 275:
                weapon.hideturtle()
                weapon.bullet_state = "ready"


if __name__ == "__main__":
    screen = Screen()
    player = Player()
    player.binding()
    weapon = Weapon()
    weapon.binding()
    enemy = Enemy()
    game = Game()
    game.run()
    turtle.done()



