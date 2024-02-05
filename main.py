from flask import Flask, request, send_from_directory, jsonify
import os
import socket
from PIL import Image

from rembg import remove
from app import principal
from addfundo import junta_img
from mostraimg import remove2,renomeia_imagem
app = Flask(__name__)


UPLOAD_FOLDER = 'input/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Verificar se a extensão do arquivo é permitida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/iaimagem', methods=['POST'])
def upload_imagem():
    if 'imagem' in request.files:
        imagem = request.files['imagem']

        if imagem.filename == '':
            return "Nenhum arquivo selecionado."

        if imagem and allowed_file(imagem.filename):
            # Obter um nome de arquivo seguro
            filename = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
            
            imagem.save(filename)
            principal(filename)

            print('¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹')

            print('Nome da imagem: ' + imagem.filename)
            print('Caminho da imagem: ' + filename)
            
            print('¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹')

            print('input/' + imagem.filename)
            
            remove2('input/' + imagem.filename, 'output/cloth_seg/final_seg.png')
           
            imagem_sem_fundo = 'output/cloth_seg/final_resultante_redimensionada.jpg'
            imagem_com_fundo = 'fundo/branco.png'
            caminho_saida = 'results'
            
            junta_img(imagem_sem_fundo, imagem_com_fundo, caminho_saida)

            caminho_imagem = 'results/final_resultante_redimensionada.png'
            filename = imagem.filename.replace('.jpg','').replace('.png','').replace('input/','')

            print('¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹')
            print('Aqui')
            print('Nome filename: ' + filename)
            print('Nome caminho_imagem: ' + caminho_imagem)
            print('¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹¹')
            renomeia_imagem(caminho_imagem, filename)
            imagem.filename = imagem.filename.replace('jpg','png')

            print(f"Link da imagem gerada http://10.0.0.50:5000/results/{imagem.filename}")


            return jsonify({"link": f"http://10.0.0.50:5000/results/{imagem.filename}"})


    return jsonify({"erro": "Arquivo não permitido ou nenhum arquivo enviado."})





@app.route('/removefundo', methods=['POST'])
def salvar_imagem():
    if 'imagem' in request.files:
        imagem = request.files['imagem']
        caminho_salvar = os.path.join('input', imagem.filename)
        imagem.save(caminho_salvar)

        try:
            input_path = 'input/' + imagem.filename
            output_path = 'resultssemfundo/' + imagem.filename

            with Image.open(input_path) as img:
                output = remove(img)

                # Converter a imagem para o modo RGB antes de salvar como JPEG
                output = output.convert("RGB")
                
                output.save(output_path, format="JPEG")

                return jsonify({"link": f"http://10.0.0.50:5000/resultssemfundo/{imagem.filename}"})


        except Exception as e:
            return jsonify({"erro ao salvar": f'Erro ao processar a imagem: {str(e)}'})

    return jsonify({"erro ao salvar " + imagem.filename + " ": "Nenhum arquivo enviado"})


output_directory = os.path.abspath('results')
@app.route('/results/<filename>')
def uploaded_image(filename):
    return send_from_directory(output_directory, filename)

output_directory = os.path.abspath('resultssemfundo')
@app.route('/resultssemfundo/<filename>')
def uploaded_image2(filename):
    return send_from_directory(output_directory, filename)


def PegaIP():
    global IPpc
    ipv4_local = obter_ipv4_local()
    if "erro" in ipv4_local.lower():
        print(f"Falha ao obter o endereço IP local: {ipv4_local}")
    else:
        print(f"Endereço IPv4 local do seu computador: {ipv4_local}")
        IPpc = ipv4_local

def obter_ipv4_local():
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        return str(e)
    
PegaIP()
app.run(port=5000, host=IPpc, debug=True)
