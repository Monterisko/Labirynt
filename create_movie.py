import imageio.v2 as imageio
import os


png_dir = './'
images = []

file_names = [f for f in os.listdir(png_dir) if f.endswith('.png')]
file_names.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))


for filename in file_names:
    images.append(imageio.imread(png_dir + filename))

imageio.mimsave('movie.gif', images, duration=1000)