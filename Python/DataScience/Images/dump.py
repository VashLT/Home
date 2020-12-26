import matplotlib.pyplot as plt
import imageio
import os
from pathlib import Path
from skimage.transform import resize
import numpy as np


COMMON_PATH = Path(
    Path.home() / "Documents" / "Home" / "Python" / "DataScience")

IMG_PATH = Path(COMMON_PATH / "Samples" / "logo.png")
MOVIE_PATH = Path(COMMON_PATH / "Samples" / "Movie.mp4")


def show_resized_comparation(resized, origin):
    titles = ["Resized image", "Original image"]
    plt.figure(figsize=(16, 16))
    for index, img in enumerate((resized, origin), 1):
        plt.subplot(1, 2, index)
        plt.imshow(resized)
        plt.title(titles[index - 1])


def read_image(path):
    img = imageio.imread(path)
    return img


def save_image(img):
    imageio.imsave(COMMON_PATH / "Samples" / "resized_img.png", img)


def process_movie():

    reader = imageio.get_reader(MOVIE_PATH)
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer(MOVIE_PATH, fps=fps)
    for im in reader:
        writer.append_data(im[:, :, 1])
    writer.close()


def resize_image():
    img = read_image(IMG_PATH)
    resize_img = resize(img, (50, 50, 3))
    show_resized_comparation(resize_img, img)
    save_image(resize_img)
    return resize_img


def main():
    exec_func = "process_movie"
    globals()[exec_func]()


if __name__ == "__main__":
    main()
