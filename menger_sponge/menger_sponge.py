import matplotlib.pyplot as plt
import numpy as np

ITERATIONS = 2
ALPHA = 0.9


def is_delete(value: int, step: int) -> bool:
    return (value // step) % 3 == 1


def drill_holes(size: int, data: np.array, iteration: int):
    step = 3 ** iteration
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if sum((is_delete(x, step), is_delete(y, step), is_delete(z, step))) >= 2:
                    data[x][y][z] = 0


def create_menger_sponge(iterations: int) -> np.array:
    size = 3 ** iterations
    axes = [size, size, size]
    data = np.ones(axes)
    for iteration in range(iterations):
        print(f'[{iteration + 1}/{iterations}]')
        drill_holes(size, data, iteration)
    return data


def draw(data: np.array, alpha: float = 1.0):
    print('drawing...')
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection='3d')
    _ = ax.voxels(
        data,
        facecolors=[0.0, 1.0, 0.0, alpha],
        edgecolors='grey',
    )
    plt.show()
    print('done')


def main():
    data = create_menger_sponge(iterations=ITERATIONS)
    draw(data, alpha=ALPHA)


if __name__ == '__main__':
    main()
