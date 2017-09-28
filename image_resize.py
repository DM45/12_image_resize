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
        'new_width': parse_params.width,
        'new_height': parse_params.height, 
        'scale': parse_params.scale
    }


def get_validation_result(
            filepath, width, height, scale):
    if scale and (width or height):
        return 'Scale and side or sides at once moment'
    if (not scale and not width and not height):
        return 'Dont have information for take new size'
    if not os.path.exists(filepath):
        return 'Wrong filepath or filename'


def get_image_with_size(filepath):
    img = Image.open(filepath)
    width, height = img.size
    return {
        'image': img,
        'width': width,
        'height': height
    }



def get_new_size(width, height, new_width, new_height, scale):
    if scale:
        scale = float(scale)
        new_width = width*scale
        new_height = height*scale
        return {
            'new_width': int(new_width), 
            'new_height': int(new_height),
        }
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
    }


def get_resized_image(width, height, old_image):
    resized_image = old_image.resize((width, height),
            Image.LANCZOS)
    return resized_image


def get_size_proportion_check(new_width, new_height, old_width, old_height):
    if new_width/int(old_width) != new_height/int(old_height):
        return 'Sizes proportion of new image is not same as the source file'


def save_image(
            filepath, width,
            height, image, 
            output):
    filename = os.path.basename(filepath)
    filename_w_o_ext, extension = os.path.splitext(filename)
    new_filename = '{}___{}x{}{}'.format(filename_w_o_ext,
        width, height, extension)
    if output:
        new_filepath = os.path.join(output, new_filename)
        image.save(new_filepath)
    else:
        image.save(new_filename)


if __name__ == '__main__':
    parse_parameters = get_parse_parameters()
    validation_result = get_validation_result(
            parse_parameters['filepath'],
            parse_parameters['new_width'],
            parse_parameters['new_height'],
            parse_parameters['scale'])
    if validation_result is None:
        image_with_size = get_image_with_size(parse_parameters['filepath'])
        new_size = get_new_size(
                image_with_size['width'],
                image_with_size['height'],
                parse_parameters['new_width'],
                parse_parameters['new_height'],
                parse_parameters['scale'])
        resized_image = get_resized_image(
                new_size['new_width'],
                new_size['new_height'],
                image_with_size['image'])
        proportion_check = get_size_proportion_check(
                new_size['new_width'],
                new_size['new_height'],
                image_with_size['width'],
                image_with_size['height'])
        if proportion_check:
            print(proportion_check)
        save_image(
                parse_parameters['filepath'],
                new_size['new_width'],
                new_size['new_height'],
                resized_image,
                parse_parameters['output'])
    else:
        print(validation_data)
