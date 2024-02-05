from rembg import remove
from PIL import Image

img = 'input/teste2.jpg'
output_path = 'results/teste2.png'

def removefundo(img):
    input = Image.open(img)
    output = remove(input)
    output.save(output_path)