from email.mime import image
import numpy as np
import cv2 as cv
import time

coordinates = []

#click event za image, da označi kvadrat in ko se levi klik zgodi se označi na sliki beli kvadratek, koordinate shrani v polje
def click_event(event, x, y, flags, param):
    global drawing, selected
    if event == cv.EVENT_LBUTTONDOWN:
        # print(x, ' ' ,y)
        coordinates.append((x, y))
        font = cv.FONT_HERSHEY_SIMPLEX
        # cv.putText(image, str(x) + ',' + str(y),(x,y),font,0.3,(255,0,0),2)
        cv.imshow('image', image)

    if event == cv.EVENT_LBUTTONUP:
        # print(x, ' ', y)
        selected = False
        coordinates.append((x, y))
        img_copy = image.copy()
        font = cv.FONT_HERSHEY_SIMPLEX
        # cv.putText(image, str(x) + ',' + str(y), (x, y), font, 0.3, (255, 0, 0), 2)

        cv.rectangle(img_copy, (coordinates[0]), (x, y), (255, 255, 255), -1)
        cv.addWeighted(img_copy, 0.5, image, 0.5, 0, image)
        cv.imshow('image', image)


#iz prej označenega okvirja izračuna povprečje vsakega kanala barve in vrne vrednosti kot numpay array, nižja in višja dovoljena vrednost
def doloci_barvo_koze(image, coordinatesS, coordinatesE):
    global coordinates
    tempR = 0.0
    tempG = 0.0
    tempB = 0.0

    xS, yS = coordinatesS
    xE, yE = coordinatesE
    xS, xE, yS, yE = int(xS), int(xE), int(yS), int(yE)

    print("xS:", xS, "xE:", xE, "yS:", yS, "yE:", yE)  # Debugging print statement

    counter = 0

    for i in range(xS, xE):
        for j in range(yS, yE):
            print("i:", i, "j:", j)  # Debugging print statement
            counter = counter + 1
            tempB = image[j, i, 0] + tempB
            tempG = image[j, i, 1] + tempG
            tempR = image[j, i, 2] + tempR

    tempR = tempR / counter
    tempG = tempG / counter
    tempB = tempB / counter

    result = np.array([[tempB - 25, tempG - 25, tempR - 25], [tempB + 25, tempG + 25, tempR + 25]]).reshape(2, 3)

    return result


#zmanjsa sliko glede na aspect ratio, da ne pokvari slike in vrne sliko
def zmanjsaj_sliko(image, sirina, visina):
    imgVisina, imgSirina = image.shape[:2]

    aspect_ratio = imgSirina / imgVisina

    if imgSirina > imgVisina:
        visina = int(sirina / aspect_ratio)
    else:
        sirina = int(visina * aspect_ratio)
    #print("Sirina: ", sirina, ' ', "Visina: ", visina)
    return cv.resize(image, (sirina, visina))

#pogleda če je vrednost znotraj nižje in višje vrednosti
def is_between(value, lower, upper):
    return lower <= value <= upper


#za vsak položaj slike se naredi škatla v za katero se prešteje koliko pokslov je barve kože
#vrne polje [[koordinata x, koordinatay y, število pikslov barve]...]
def obdelaj_sliko_s_skatlami(image, sirina_skatle, visina_skatle, color):
    imgVisina, imgSirina = image.shape[:2]

    data = []

    for x in range(0, imgSirina, sirina_skatle):
        for y in range(0, imgVisina, visina_skatle):
            subimage = image[y:y + visina_skatle, x:x + sirina_skatle]
            counter=prestej_piksle_z_barvo_koze(subimage,color)
            row = [x,y, counter]
            data.append(row)

    array = np.array(data)

    return array


#za vsako škatlo/sliko, ki pride prešteje koliko pikslov je barve kože
def prestej_piksle_z_barvo_koze(image,color):
    imgVisina, imgSirina = image.shape[:2]

    colorBs, colorGs, colorRs = color[0]
    colorBe, colorGe, colorRe = color[1]

    counter = 0

    for i in range(imgSirina):
        for j in range(imgVisina):
            if (is_between(image[j, i, 0], colorBs, colorBe) and
                    is_between(image[j, i, 1], colorGs, colorGe) and
                    is_between(image[j, i, 2], colorRs, colorRe)):
                counter += 1

    return counter


def display_frames(image, fps):


if __name__ == '__main__':
