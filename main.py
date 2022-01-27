from utils import resize
import argparse

if __name__ == '__main__':
    try:
        resize.mask_resize('./sample/original/img1.jpg', width=350, height=270, image_folder='./sample/convert',
                           anchor_point='BR')
        resize.mask_resize('./sample/original/img2.jpg', width=350, height=270, image_folder='./sample/convert',
                           anchor_point='BR')
    except FileNotFoundError as e:
        print(f'File not found error: {e}')
    except Exception as e:
        print(f'Resize image exception: {e}')