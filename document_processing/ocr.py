import pytesseract
from PIL import Image
import argparse

def ocr_image(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input image/pdf path")
    parser.add_argument("--output", required=True, help="Output text file path")
    args = parser.parse_args()

    text = ocr_image(args.input)
    with open(args.output, "w") as f:
        f.write(text)
