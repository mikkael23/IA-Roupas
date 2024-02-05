from PIL import Image, ExifTags
import torch
import gradio as gr
from process import load_seg_model, get_palette, generate_mask

device = 'cpu'

def initialize_and_load_models():
    checkpoint_path = 'model/cloth_segm.pth'
    net = load_seg_model(checkpoint_path, device=device)
    return net

net = initialize_and_load_models()
palette = get_palette(4)

def run(img):
    # Corrige a orientação da imagem se necessário
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break

    try:
        exif=dict(img._getexif().items())
        if exif[orientation] == 3:
            img=img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img=img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img=img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # A imagem não tem informações de orientação EXIF
        pass

    cloth_seg = generate_mask(img, net=net, palette=palette, device=device)
    return cloth_seg

def principal(imagem):
    img = Image.open(imagem)
    result = run(img)
    return result
