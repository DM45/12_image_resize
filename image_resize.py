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
    parse_params = parser.parse_args()
    return {
        'filepath': parse_params.filepath,
        'output': parse_params.output,
        'width': parse_params.width,
        'height': parse_params.height, 
        'scale': parse_params.scale
    }


def get_validation_data(
            param_filepath, param_width, param_height, param_scale):
    if param_scale and (param_width or param_height):
        return 'Scale and side or sides at once moment'
    if (not param_scale and not param_width and not param_height):
        return 'Dont have information for take new size'
    if not os.path.exists(param_filepath):
        return 'Wrong filepath or filename'


def get_new_size(param_filepath, param_width, param_height, param_scale):
    img = Image.open(param_filepath)
    width, height = img.size
    if param_scale:
        scale = float(param_scale)
        new_width = width*scale
        new_height = height*scale
        return {
            'new_width': int(new_width), 
            'new_height': int(new_height),
            'old_image': img, 
            'old_width': int(width),
            'old_height': int(height)
        }
    new_width = param_width
    new_height = param_height
    try:
        new_width = float(new_width)
    except TypeError:
        new_width = width*float(new_height)/height
    try:
        new_height = float(new_height)
    except TypeError:
        new_height = float(new_width)*height/width
    return {
        'new_width': int(new_width), 
        'new_height': int(new_height),
        'old_image': img, 
        'old_width': width,
        'old_height': height
    }


def get_resize_image(new_width, new_height, old_image):
    new_image = old_image.resize((new_width, new_height),
            Image.LANCZOS)
    return new_image


def get_size_proportion_check(new_width, new_height, old_width, old_height):
    if new_width/int(old_width) != new_height/int(old_height):
        return 'Sizes proportion of new image is not the same as the source file'


def save_new_image_as_file(
            param_filepath, new_width,
            new_height, new_image, 
            param_output):
    filename = os.path.basename(param_filepath)
    filename_w_o_ext, extension = os.path.splitext(filename)
    new_filename = '{}___{}x{}{}'.format(filename_w_o_ext,
        new_width, new_height, extension)
    if param_output:
        new_filepath = os.path.join(param_output, new_filepath)
        new_image.save(new_filepath)
    else:
        new_image.save(new_filename)


if __name__ == '__main__':
    parse_parameters = get_parse_parameters()
    validation_data = get_validation_data(
            parse_parameters['filepath'],
            parse_parameters['width'],
            parse_parameters['height'],
            parse_parameters['scale'])
    if validation_data is None:
        new_size = get_new_size(
                parse_parameters['filepath'],
                parse_parameters['width'],
                parse_parameters['height'],
                parse_parameters['scale'])
        resize_image = get_resize_image(
                new_size['new_width'],
                new_size['new_height'],
                new_size['old_image'])
        proportion_check = get_size_proportion_check(
                new_size['new_width'],
                new_size['new_height'],
                new_size['old_width'],
                new_size['old_height'])
        if proportion_check:
            print(proportion_check)
        save_new_image_as_file(
                parse_parameters['filepath'],
                new_size['new_width'],
                new_size['new_height'],
                resize_image,
                parse_parameters['output'])
    else:
        print(validation_data)
