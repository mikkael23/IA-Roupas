import cv2
import os
def exibir_imagem(caminho_imagem, largura_desejada=300):
    try:
        # Carregar a imagem
        imagem = cv2.imread(caminho_imagem)

        # Certificar-se de que a imagem foi carregada corretamente
        if imagem is None:
            print(f"Erro ao carregar a imagem em: {caminho_imagem}")
            return

        # Obter as dimensões originais da imagem
        altura, largura = imagem.shape[:2]

        # Calcular a proporção de redimensionamento
        proporcao = largura_desejada / largura
        nova_altura = int(altura * proporcao)

        # Redimensionar a imagem
        imagem_redimensionada = cv2.resize(imagem, (largura_desejada, nova_altura))

        # Exibir a imagem redimensionada
        cv2.imshow(f"Imagem (Largura: {largura_desejada})", imagem_redimensionada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Erro ao exibir a imagem: {e}")




def remove2(caminho_imagem_original, caminho_imagem_mascara, largura_exibicao=500):
    # Carregar a imagem original
    imagem_original = cv2.imread(caminho_imagem_original)
    
    # Carregar a imagem da máscara em escala de cinza
    imagem_mascara = cv2.imread(caminho_imagem_mascara, cv2.IMREAD_GRAYSCALE)

    # Verificar se as imagens foram carregadas corretamente
    if imagem_original is None or imagem_mascara is None:
        print("Erro ao carregar uma das imagens.")
        return

    # Converter a máscara para um formato binário (preto e branco)
    _, imagem_mascara_binaria = cv2.threshold(imagem_mascara, 1, 255, cv2.THRESH_BINARY)

    # Aplicar a máscara binária na imagem original
    imagem_resultante = cv2.bitwise_and(imagem_original, imagem_original, mask=imagem_mascara_binaria)

    # Redimensionar a imagem para largura_exibicao pixels
    altura_exibicao = int(largura_exibicao / imagem_original.shape[1] * imagem_original.shape[0])
    imagem_resultante_redimensionada = cv2.resize(imagem_resultante, (largura_exibicao, altura_exibicao))

    # Mostrar a imagem resultante redimensionada
    # cv2.imshow("Imagem Resultante", imagem_resultante_redimensionada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    caminho_saida = 'output/cloth_seg/final_resultante_redimensionada.jpg'
    cv2.imwrite(caminho_saida, imagem_resultante_redimensionada)

def renomeia_imagem(caminho_imagem, novo_nome):
                try:
                    if os.path.exists(caminho_imagem):
                        diretorio, nome_extensao = os.path.split(caminho_imagem)
                        nome_base, extensao = os.path.splitext(nome_extensao)
                        
                        novo_caminho = os.path.join(diretorio, f'{novo_nome}{extensao}')
                        os.rename(caminho_imagem, novo_caminho)
                        print(f"Imagem renomeada para: {novo_caminho}")
                    else:
                        print(f"Erro: O arquivo {caminho_imagem} não existe.")
                except Exception as e:
                    print(f"Erro ao renomear a imagem: {str(e)}")


