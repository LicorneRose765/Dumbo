from . import dumbo
import sys


if __name__ == "__main__":
    if len(sys.argv) != 1:
        if len(sys.argv) != 3:
            print('Usage: python3 dumbo.py <data> <template>')
            exit(1)
        data_path = sys.argv[1]
        template_path = sys.argv[2]
        dumbo.parse_data_template(data_path, template_path)
