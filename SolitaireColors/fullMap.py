from PIL import Image
import os
out_path = './SolitaireColors/Image/'
in_path = 'E:/Fisker/Downloads/map/Sprite/'


def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


map_num = 61
image_num = 20

for map_index in range(map_num):
    out_file = f'{out_path}bg_map_full/bg_map_full_{str(map_index+ 51)}.png'
    im1_file = f'{in_path}map{map_index+51}_1.png'
    if os.path.exists(im1_file):
        im1 = Image.open(im1_file)
        for i in range(image_num-1):
            im2_file = f'{in_path}map{map_index+51}_{str(i + 2)}.png'
            if not os.path.exists(im2_file):
                break
            im2 = Image.open(im2_file)
            print('merge', map_index+51, im2_file)
            im1 = merge(im1, im2)
        print("*"*20, 'save', out_file)
        im1.save(out_file, "png")
