import sys

sys.path.insert(0, './commons')
import file_handling as fH  # noqa

if len(sys.argv) < 2:
    print("Usage: python merge_pieces_to_spritesheet.py xcom-extracted-images-folder")  # noqa
    sys.exit(0)

path = sys.argv[1]

fileList = []
fileList = fH.populateFileList(path, fileList, [".gif"])

print(fileList)
