import argparse
import os
from PIL import Image


def get_parse_parameters():
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('filepath', metavar='FilePath')
    parser.add_argument('--output')
    parser.add_argument('--width')
    parser.add_argument('--height')
    parser.add_argument('--scale')
    return parser.parse_args()


def get_errors_check_with_output(parse_parameters):
    if parse_parameters.scale and (parse_parameters.width
            or parse_parameters.height):
        print('Scale and side or sides at once moment')
        return 'Error'
    if (not parse_parameters.scale and not parse_parameters.width
            and not parse_parameters.height):
        print('Dont have information for take new size')
        return 'Error'
    if not os.path.exists(parse_parameters.filepath):
        print('Wrong filepath or filename')
        return 'Error'


def get_new_size(parse_parameters):
    img = Image.open(parse_parameters.filepath)
    width, height = img.size
    if parse_parameters.scale:
        scale = float(parse_parameters.scale)
        new_width_sc = width*scale
        new_height_sc = height*scale
        return (int(new_width_sc), int(new_height_sc),
                img, width, height)
    new_width = parse_parameters.width
    new_height = parse_parameters.height
    try:
        new_width = float(new_width)
    except TypeError:
        new_width = width*float(new_height)/height
    try:
        new_height = float(new_height)
    except TypeError:
        new_height = float(new_width)*height/width
    return int(new_width), int(new_height), img, width, height


def get_resize_image(new_width, new_height, old_image):
    new_image = old_image.resize((new_width, new_height),
            Image.LANCZOS)
    return new_image


def get_proportion_check(new_width, new_height, old_width, old_height):
    if new_width/old_width != new_height/old_height:
        print('Proportion is not the same as the source file')


def save_new_image(parse_parameters, new_width,
        new_height, old_image, new_image):
    width, height = old_image.size
    filepath = parse_parameters.filepath
    filename = os.path.basename(filepath)
    filename_w_o_ext = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    output_filepath = parse_parameters.output
    new_filename = '{}{}{}{}{}{}'.format(filename_w_o_ext,
        '___', new_width, 'x', new_height, extension)
    if output_filepath:
        new_filepath = os.path.join(output_filepath, new_filepath)
        new_image.save(new_filepath)
    else:
        new_image.save(new_filename)


if __name__ == '__main__':
    parse_parameters = get_parse_parameters()
    if get_errors_check_with_output(parse_parameters) is None:
        new_size = get_new_size(parse_parameters)
        resize_image = get_resize_image(new_size[0], new_size[1], new_size[2])
        proportion_check = get_proportion_check(new_size[0],
                new_size[1], new_size[3], new_size[4])
        save_new_image(parse_parameters, new_size[0], new_size[1], new_size[2],
                resize_image)
