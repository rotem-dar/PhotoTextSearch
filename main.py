import sys
import pytesseract
import cv2
import os
import shutil

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
input_folder = 'input_images'  # directory for input images to search through
output_folder = 'output_images' # directory for output images
keyword_search = ''

if len(sys.argv) < 2:
    print("Usage: python main.py <search_keyword>")
    sys.exit(1)
elif sys.argv[1] == '-h':
    print("Input your photos inside 'input_images' folder, then:\n"
          "Usage: python main.py <search_keyword>\n"
          "That's it! no further arguments accepted.\n"
          "Note: Each time you run the program, the output_folder is erased.\n"
          "If you want to keep it, you should change its name before running the "
          "program again.")
    sys.exit(1)
else:
    keyword_search = sys.argv[1]
    # deletes the directory if it already exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    # Recreate it
    os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        image_path = os.path.join(input_folder, filename)

        # Load image
        img = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply threshold (black & white)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # OCR
        text = pytesseract.image_to_string(thresh)
        text_list = text.split('\n')

        for line in text_list:
            if keyword_search.lower() in line.lower():
                print(f'"{filename}" >> \033[34m{line}\033[0m')
                shutil.copy(image_path, output_folder)

        # print(text)