import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import json
from tqdm import trange, tqdm

def read_files(path):
  '''
  Function for reading all the folders in the directory

  path: path of the directory
  list_files: a list of all the files in that directory.
  '''

  files = os.listdir(path)
  list_files = []
  name_files = []

  # for each folder in the path, joins the directory and saves it in a list
  for file in files:
    name_files.append(file)
    new_file = os.path.join(path, file)
    list_files.append(new_file)

  return list_files, name_files

def detect_colors(arr1,tol):

    # confirmamos que los arreglios sean del mismo tamaño
    ''''''''''
    if (len(arr1) != 3):
        print('No es un arreglo valido')
        return None
    '''
    max_num = np.max(arr1)

    # Separamos los valores del arreglo
    num_1 = arr1[0]
    num_2 = arr1[1]
    num_3 = arr1[2]



    # Obtenemos la comparacion entre ellos
    val_1 = np.isclose(num_1, max_num, atol=tol)
    val_2 = np.isclose(num_2, max_num, atol=tol)
    val_3 = np.isclose(num_3, max_num, atol=tol)

    color_lane = [val_1, val_2 , val_3]

    color_eval = [[False, False, True], [False, True, False], [True, False, False], [False, True, True], [True, True, True]]
    color_name = ['azul','verde','rojo','amarillo','blanco']

    for i in range(len(color_eval)):

        if color_eval[i] == color_lane:
            color_value = color_name[i]

            if color_value == None:
                print('ah caray')

            return color_value

def obtener_carriles(img):


    vals = np.unique(img)
    # Ajustando los valores:
    img[img > 200] = 255
    img[img < 100] = 0



    # Declracion de los carriles.
    color_rojo = []
    color_azul = []
    color_verde = []
    color_amarillo = []
    color_blanco = []

    # Loop principal para recorrer la imagen verticalmente y luego horizontal buscando los carrles.
    for i in range(160,720,10):
        #print('--------',i,'--------')

        color_coordenada = [] # Almacena el color de carril
        color_name = ['azul','verde','rojo','amarillo','blanco']

        for j in range(1280):
            valores = img[i][j]

            if ( np.max(valores) > 10):
                carriles = True
                color = detect_colors(valores,25)

                if color == None:
                    color_azul.append(-2)
                    color_rojo.append(-2)
                    color_verde.append(-2)
                    color_amarillo.append(-2)
                    color_blanco.append(-2)
                    break

                if color not in color_coordenada:

                    color_name.remove(color)
                    color_coordenada.append(color)

                    if color == 'azul':
                        color_azul.append(j)

                    if color == 'rojo':
                        color_rojo.append(j)

                    if color == 'amarillo':
                        color_amarillo.append(j)

                    if color == 'verde':
                        color_verde.append(j)

                    if color == 'blanco':
                        color_blanco.append(j)

                #print((color), (i, j))

        for color_falt in color_name:

            if color_falt == 'azul':
                color_azul.append(-2)

            if color_falt == 'rojo':
                color_rojo.append(-2)

            if color_falt == 'amarillo':
                color_amarillo.append(-2)

            if color_falt == 'verde':
                color_verde.append(-2)

            if color_falt == 'blanco':
                color_blanco.append(-2)

    while len(color_rojo) > 56:
        color_rojo.pop(-1)
        color_azul.pop(-1)
        color_amarillo.pop(-1)
        color_blanco.pop(-1)
        color_verde.pop(-1)

    return  color_rojo, color_verde, color_azul, color_amarillo,  color_blanco

def createJson(path_img,json_path):
    # Data to be written
    hsamples = [160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710]

    # Datos
    path_img = r'D:\Maestria\Checkpoint\prediccion_color_skeleton\\'

    list_files, name_files = read_files(path_img)

    dim = (1280,720)

    for i in tqdm(range(len(list_files))):
        # Cargar imagen
        img = cv2.imread(list_files[i])
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,dim, interpolation = cv2.INTER_AREA)

        carr_1 , carr_2 , carr_3 , carr_4, carr_5 = obtener_carriles(img)

        carr_total = []

        if len(np.unique(carr_1)) != 1:
            carr_total.append(carr_1)

        if len(np.unique(carr_2)) != 1:
            carr_total.append(carr_2)

        if len(np.unique(carr_3)) != 1:
            carr_total.append(carr_3)

        if len(np.unique(carr_4)) != 1:
            carr_total.append(carr_4)

        if len(np.unique(carr_5)) != 1:
            carr_total.append(carr_5)

        # Quitar el .jpg duplicado de los nombres
        old_str = name_files[i]
        new_str = old_str[:-4]

        dictionary = {
            "lanes": carr_total,
            "h_samples": hsamples,
            "raw_file": new_str,
            "run_time": "1"
        }

        # Serializing json
        json_object = json.dumps(dictionary)

        if i == 0:
            with open(json_path, "w") as outfile:
                outfile.write(json_object)
        else:
            with open(json_path, "a") as outfile:
                outfile.write('\n')
                outfile.write(json_object)
