import os
import re
import hashlib
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

os.system('cls')

def encontrar_duplicados(diretorio):
    # Dicionário para armazenar hashes e arquivos correspondentes
    hashes = {}
    duplicados = []

    # Percorre todos os arquivos no diretório
    for pasta_raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_raiz, arquivo)

            # Calcula o hash do arquivo
            with open(caminho_completo, "rb") as f:
                hash_arquivo = hashlib.md5(f.read()).hexdigest()

            # Se o hash já existir no dicionário, o arquivo é um duplicado
            if hash_arquivo in hashes:
                duplicados.append(caminho_completo)
            else:
                hashes[hash_arquivo] = caminho_completo

    return duplicados

def mover_duplicados(duplicados, pasta_destino):
    # Cria a pasta de destino se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Move os arquivos duplicados para a pasta de destino
    for arquivo in duplicados:
        shutil.move(arquivo, pasta_destino)
        print(f"Movendo arquivo! - {arquivo}")

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = {}
    if hasattr(image, '_getexif'):
        exif_info = image._getexif()
        if exif_info is not None:
            for tag, value in exif_info.items():
                tag_name = TAGS.get(tag, tag)
                exif_data[tag_name] = value
    return exif_data

def get_image_datetime(image_path):
    exif_data = get_exif_data(image_path)
    datetime_str = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
    if datetime_str:
        # Formatando a data e a hora para um formato adequado para o nome do arquivo
        datetime_str = datetime_str.replace(":", "").replace(" ", "_")
    return datetime_str

def remove_parentheses_from_filenames(directory):
    for filename in os.listdir(directory):
        old_file = os.path.join(directory, filename)
        if not os.path.isfile(old_file):
            continue
        
        # Obtém a data e hora da imagem
        datetime_str = get_image_datetime(old_file)
        if not datetime_str:
            print(f"Data e hora não encontradas para {filename}")
            continue
        
        # Remove parênteses do nome do arquivo e adiciona a data e hora
        base, extension = os.path.splitext(filename)
        new_filename = f"{datetime_str}{extension}"
        new_file = os.path.join(directory, new_filename)
        
        # Verifica se o novo nome de arquivo já existe
        if os.path.exists(new_file):
            # Pode adicionar um sufixo ou número ao novo nome do arquivo para torná-lo único
            counter = 10
            while os.path.exists(new_file):
                new_file = os.path.join(directory, f"{datetime_str}_{counter}{extension}")
                counter += 1

        # Renomeia o arquivo
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_file}')

if __name__ == "__main__":
    print('Inicio do programa.')
    # Diretório a ser verificado \\
    diretorio = fr"DIRETORIO DA PASTA PARA QUAL O CODIGO VAI SER EXECUTADO"
        
    duplicados = encontrar_duplicados(diretorio)

    if duplicados:
        # Pasta para mover os arquivos duplicados
        pasta_destino = os.path.join(diretorio, "duplicados")

        # Move os arquivos duplicados para a pasta de destino
        mover_duplicados(duplicados, pasta_destino)
        print("Arquivos duplicados movidos para:", pasta_destino)
    else:
       print("Nenhum arquivo duplicado encontrado.")

    remove_parentheses_from_filenames(diretorio)
    print('Fim do programa.')

