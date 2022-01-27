import glob

from PIL import Image
import os

TMP_FOLDER = "./sample/tmp"


def get_path(source_path, dest_folder=None):
    image_basename = os.path.basename(source_path)
    return source_path if dest_folder is None else dest_folder + "/" + image_basename


def resize(image_path, width=0, height=0, image_folder=None):
    if width == 0 and height == 0:
        raise Exception('Both width and height are auto! Wtf :)')

    img = Image.open(image_path)
    width_image, height_image = img.size

    if width == 0:
        width = int(height * width_image / height_image)

    if height == 0:
        height = int(width * height_image / width_image)

    if width > width_image:
        width = width_image

    if height > height_image:
        height = height_image

    resized_image = img.resize((width, height))
    path = get_path(image_path, image_folder)
    resized_image.save(path)
    return path


def calculate_resize_by(image_path, width, height):
    img = Image.open(image_path)
    width_image, height_image = img.size

    ''' by width, calculate height '''

    resize_height = int(height_image * width / width_image)
    print(f'by width, resize_height should be {resize_height}')

    ''' by height, calculate width '''

    resize_width = int(width_image * height / height_image)
    print(f'by height, resize_width should be {resize_width}')

    return ('width', resize_height) if resize_height > height else ('height', resize_width)


def get_crop_points(image_path, width, height, anchor_point='CC'):
    img = Image.open(image_path)
    width_image, height_image = img.size

    if anchor_point == 'TL':
        return 0, 0, width, height
    if anchor_point == 'TC':
        offset = int(abs(width_image - width) / 2)
        print(f'> calculated offset {offset} for anchor point {anchor_point}')
        return offset, 0, int(abs(width_image - offset)), height
    if anchor_point == 'TR':
        offset = int(abs(width_image - width))
        print(f'> calculated offset {offset} for anchor point {anchor_point}')
        return offset, 0, width_image, height
    if anchor_point == 'CL':
        offset = int(abs(height_image - height) / 2)
        print(f'> calculated offset {offset} for anchor point {anchor_point}')
        return 0, offset, width, int(abs(height_image - offset))
    if anchor_point == 'CR':
        offset = int(abs(height_image - height) / 2)
        print(f'> calculated offset {offset} for anchor point {anchor_point}')
        return int(abs(width_image - width)), offset, width_image, int(abs(height_image - offset))
    if anchor_point == 'BL':
        return 0, int(abs(height_image - height)), width, height_image
    if anchor_point == 'BC':
        offsetWidth = int(abs(width_image - width) / 2)
        return offsetWidth, 0, int(abs(width_image - offsetWidth)), height
    if anchor_point == 'BR':
        return int(abs(width_image - width)), int(abs(height_image - height)), width_image, height_image

    ''' anchor_point CC'''
    offset = int(abs(width_image - width) / 2)
    offsetTop = int(abs(height_image - height) / 2)
    return offset, int(abs(height_image - height) / 2), int(abs(width_image - offset)), int(
        abs(height_image - offsetTop))


def crop(image_path, width, height, anchor_point='CC', image_folder=None):
    points = get_crop_points(image_path, width, height, anchor_point)
    print(f'Selected points {points} from anchor point {anchor_point}, path={image_path}')

    img = Image.open(image_path)
    cropped_image = img.crop(points)
    path = get_path(image_path, image_folder)
    cropped_image.save(path)
    return path


def mask_resize(image_path, width, height, image_folder=None, anchor_point='CC'):
    if width == 0 or height == 0:
        raise Exception('Both width and height should be compiled! Wtf :)')

    print(f'Load image from {image_path}')

    by, op_value = calculate_resize_by(image_path, width, height)

    print(f'by={by}, op_value={op_value}')

    ''' intermediary resize '''

    intermediate_path = resize(image_path, 0 if by == 'height' else width, 0 if by == 'width' else height, TMP_FOLDER)

    print(f'Saved intermediate image in {intermediate_path}')

    definitive_path = crop(intermediate_path, width, height, anchor_point, image_folder)

    os.remove(intermediate_path)

    print(f'Saved definitive image in {definitive_path}')

    return definitive_path


def bulk_action(action, source, destination, attrs):
    for file in glob.glob(f"{source}/*.jpg"):
        single_action(action, file, destination, attrs)


def single_action(action, source, destination, attrs):
    if action == 'resize':
        resize(image_path=source, image_folder=destination, width=attrs['width'], height=attrs['height'])
    if action == 'mask_resize':
        mask_resize(image_path=source, image_folder=destination, width=attrs['width'], height=attrs['height'],
                    anchor_point=attrs['anchor_point'])
