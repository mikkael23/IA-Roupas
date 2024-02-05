from rembg import remove as rembg_remove
import os
from PIL import Image

def junta_img(imagem_sem_fundo, imagem_com_fundo, caminho_saida):
    # Carregar imagens
    img_sem_fundo = Image.open(imagem_sem_fundo)
    img_com_fundo = Image.open(imagem_com_fundo)
    
    # Remover fundo da imagem sem fundo
    output_img = rembg_remove(img_sem_fundo)
    img_sem_fundo = output_img.convert("RGBA")

    # Converter imagem com fundo para RGBA
    img_com_fundo = img_com_fundo.convert("RGBA")

    # Redimensionar a imagem sem fundo para a altura desejada e ajustar a largura proporcionalmente
    altura_desejada = 1080
    img_sem_fundo = img_sem_fundo.resize((int((altura_desejada / img_sem_fundo.size[1]) * img_sem_fundo.size[0]), altura_desejada))

    # Obter dimensões das imagens
    largura_sem_fundo, altura_sem_fundo = img_sem_fundo.size
    largura_com_fundo, altura_com_fundo = img_com_fundo.size

    # Determinar as dimensões da nova imagem
    nova_largura = max(largura_sem_fundo, largura_com_fundo)
    nova_altura = max(altura_sem_fundo, altura_com_fundo)

    # Criar nova imagem com fundo branco
    nova_imagem = Image.new('RGBA', (nova_largura, nova_altura), (255, 255, 255, 0))

    # Calcular deslocamento para centralizar a imagem sem fundo
    x_offset = (nova_largura - largura_sem_fundo) // 2
    y_offset = (nova_altura - altura_sem_fundo) // 2

    # Colar a imagem com fundo na nova imagem
    nova_imagem.paste(img_com_fundo, (0, 0), img_com_fundo)

    # Colar a imagem sem fundo na nova imagem, com deslocamento
    nova_imagem.paste(img_sem_fundo, (x_offset, y_offset), img_sem_fundo)

    # Criar caminho completo para salvar a nova imagem
    nome_arquivo = os.path.splitext(os.path.basename(imagem_sem_fundo))[0]
    caminho_saida_completo = os.path.join(caminho_saida, f'{nome_arquivo}.png')

    # Certificar-se de que o diretório de saída existe
    if not os.path.exists(caminho_saida):
        os.makedirs(caminho_saida)

    # Salvar a nova imagem
    nova_imagem.save(caminho_saida_completo, format="PNG")