
import argparse
from utils.cli import is_dir
from utils.resize import bulk_action, single_action

if __name__ == '__main__':

    cli_parser = argparse.ArgumentParser(description='Python Image Tools')
    cli_parser.add_argument('--action', required=True, help='Action to do', choices=['resize', 'mask_resize'])
    cli_parser.add_argument('--source', required=True, help='Source path (file path or folder)')
    cli_parser.add_argument('--width', required=False, help='Image width', type=int, default=0)
    cli_parser.add_argument('--height', required=False, help='Image height', type=int, default=0)
    cli_parser.add_argument('--destination', required=True, help='Destination folder')
    cli_parser.add_argument('--anchor-point', required=False, help='Anchor point', default='CC', choices=['TL', 'TC',
                                                                                                          'TR', 'CL',
                                                                                                          'CC', 'CR',
                                                                                                          'BL', 'BC',
                                                                                                          'BR'])

    args = cli_parser.parse_args()

    action = args.action
    source = args.source
    destination = args.destination

    try:

        attrs = {
                "width": args.width,
                "height": args.height,
                "anchor_point": args.anchor_point
            }

        if is_dir(source):
            print(f'BULK {source}')
            bulk_action(action, source, destination, attrs)
        else:
            single_action(action, source, destination, attrs)

    except FileNotFoundError as e:
        print(f'File not found error: {e}')
    except Exception as e:
        print(f'Resize image exception: {e}')
