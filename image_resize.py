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
    pars_param = parser.parse_args()
    return [
        pars_param.filepath, pars_param.output,
        pars_param.width, pars_param.height, pars_param.scale
        ]


def get_errors_check_with_output(
            par_filepath, par_width, par_height, par_scale):
    if par_scale and (par_width or par_height):
        return 'Scale and side or sides at once moment'
    if (not par_scale and not par_width and not par_height):
        return 'Dont have information for take new size'
    if not os.path.exists(par_filepath):
        return 'Wrong filepath or filename'


def get_new_size(par_filepath, par_width, par_height, par_scale):
    img = Image.open(par_filepath)
    width, height = img.size
    if par_scale:
        scale = float(par_scale)
        new_width_sc = width*scale
        new_height_sc = height*scale
        return int(new_width_sc), int(
                new_height_sc), img, int(width), int(height)
    new_width = par_width
    new_height = par_height
    try:
        new_width = float(new_width)
    except TypeError:
        new_width = width*float(new_height)/height
    try:
        new_height = float(new_height)
    except TypeError:
        new_height = float(new_width)*height/width
    return int(new_width), int(new_height), img, int(width), int(height)


def get_resize_image(new_width, new_height, old_image):
    new_image = old_image.resize((new_width, new_height),
            Image.LANCZOS)
    return new_image


def get_proportion_check(new_width, new_height, old_width, old_height):
    if new_width/old_width != new_height/old_height:
        return 'Proportion is not the same as the source file'


def save_new_image(
            par_filepath, new_width,
            new_height, old_image, 
            new_image, par_output):
    width, height = old_image.size
    filename = os.path.basename(par_filepath)
    filename_w_o_ext = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    output_filepath = par_output
    new_filename = '{}___{}x{}{}'.format(filename_w_o_ext,
        new_width, new_height, extension)
    if output_filepath:
        new_filepath = os.path.join(output_filepath, new_filepath)
        new_image.save(new_filepath)
    else:
        new_image.save(new_filename)


if __name__ == '__main__':
    parse_parameters = get_parse_parameters()
    errors_check_with_output = get_errors_check_with_output(
        parse_parameters[0], parse_parameters[2],
        parse_parameters[3], parse_parameters[4]
        )
    if errors_check_with_output is None:
        new_size = get_new_size(parse_parameters[0], parse_parameters[2],
            parse_parameters[3], parse_parameters[4])
        resize_image = get_resize_image(new_size[0], new_size[1], new_size[2])
        proportion_check = get_proportion_check(new_size[0],
                new_size[1], new_size[3], new_size[4])
        if proportion_check:
            print(proportion_check)
        save_new_image(parse_parameters[0], new_size[0], new_size[1],
            new_size[2], resize_image, parse_parameters[1])
    else:
        print(errors_check_with_output)
