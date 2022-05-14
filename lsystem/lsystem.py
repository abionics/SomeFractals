import random
from dataclasses import dataclass
from turtle import Turtle


class LSystem:

    def __init__(self, axiom: str, rules: dict[str, str]):
        self._check_rules(rules)  # all rules must be upper case
        self.axiom = axiom
        self.rules = rules

    @staticmethod
    def _check_rules(rules: dict[str, str]):
        for old, new in rules.items():
            count = sum(ch.islower() for ch in old) + sum(ch.islower() for ch in new)
            assert count == 0, f'There are {count} lowercase symbols: {old=}, {new=}'

    def generate(self, iterations: int) -> str:
        current_formula = self.axiom
        for i in range(iterations):
            for old, new in self.rules.items():
                # use lowercase in order to skip circular dependencies
                current_formula = current_formula.replace(old, new.lower())
            current_formula = current_formula.upper()
        return current_formula


@dataclass
class State:
    x: float
    y: float
    a: float
    angle: float
    length: float
    width: float


class Drawer:

    def __init__(self, formula: str, angle: float, start_length: float, start_width: float):
        self.formula = formula
        self.angle = angle
        self.length = start_length
        self.width = start_width
        self.stack = list()
        self.pen = self._create_pen()

    @staticmethod
    def _create_pen() -> Turtle:
        pen = Turtle()
        pen.up()
        pen.hideturtle()
        pen._tracer(0, 0)  # noqa very fast draw
        pen.setheading(90)
        pen.sety(-100)
        return pen

    def draw(self):
        for symbol in self.formula:
            self.apply(symbol)
        self.pen.getscreen().exitonclick()

    def apply(self, symbol: str):
        match symbol:
            case 'F':
                self.forward()
            case '+':
                self.right()
            case '-':
                self.left()
            case '[':
                self.put()
            case ']':
                self.pop()

    def forward(self):
        self._next_length()
        self._next_width()
        self.pen.width(self.width)
        self.pen.down()
        self.pen.forward(self.length)
        self.pen.up()

    def right(self):
        self._next_angle()
        self.pen.right(self.angle)

    def left(self):
        self._next_angle()
        self.pen.left(self.angle)

    def put(self):
        state = State(self.pen.xcor(), self.pen.ycor(), self.pen.heading(), self.angle, self.length, self.width)
        self.stack.append(state)

    def pop(self):
        state = self.stack.pop()
        self.pen.goto(state.x, state.y)
        self.pen.setheading(state.a)
        self.angle = state.angle
        self.length = state.length
        self.width = state.width

    def _next_length(self):
        multiplier = random.triangular(0.6, 0.9, random.gauss(0.8, 0.1))
        self.length *= multiplier

    def _next_width(self):
        multiplier = random.triangular(0.5, 1, random.gauss(0.8, 0.1))
        self.width *= multiplier

    def _next_angle(self):
        self.angle += random.triangular(-7.5, 7.5, random.gauss(0, 2))


def main():
    l_system = LSystem(
        axiom='A',
        rules={
            'A': 'F[+A][-A]',
        },
    )
    formula = l_system.generate(iterations=10)
    drawer = Drawer(formula, angle=25, start_length=100, start_width=6)
    drawer.draw()


if __name__ == '__main__':
    main()
