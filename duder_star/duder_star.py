import math

import matplotlib.pyplot as plt

ITERATIONS = 5


def create_duder_start(x: float, y: float, radius: float, angle: float, iteration: int, data: list):
    pi5 = math.pi / 5
    h = 2 * radius * math.cos(pi5)

    for i in range(5):
        ang2 = angle + pi5 * i * 2
        x2 = x - h * math.cos(ang2)
        y2 = y - h * math.sin(ang2)
        rad2 = radius / (2 * math.cos(pi5) + 1)
        ang3 = angle + math.pi + (2 * i + 1) * pi5
        for j in range(1):
            start = (
                x + rad2 * math.cos(ang3 + j * pi5 * 2),
                y + rad2 * math.sin(ang3 + j * pi5 * 2),
            )
            finish = (
                x + rad2 * math.cos(ang3 + (j + 1) * pi5 * 2),
                y + rad2 * math.sin(ang3 + (j + 1) * pi5 * 2),
            )
            data.append((start, finish))

            if iteration > 0:
                sub_radius = radius / (2 * math.cos(pi5) + 1)
                sub_angle = angle + math.pi + (2 * i + 1) * pi5
                create_duder_start(x2, y2, sub_radius, sub_angle, iteration - 1, data)


def draw(data: list):
    print('drawing...')
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()
    for (x1, y1), (x2, y2) in data:
        ax.plot((x1, x2), (y1, y2), color='black')
    plt.show()
    print('done')


def main():
    data = list()
    create_duder_start(0, 0, 10, angle=0, iteration=ITERATIONS, data=data)
    draw(data)


if __name__ == '__main__':
    main()
