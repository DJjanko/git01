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
    #preveri kamero, izberemo kvadrat
    kamera = cv.VideoCapture(0)
    if not kamera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        selected = True
        ret, image = kamera.read()
        while selected:
            cv.imshow('image', image)
            cv.setMouseCallback('image', click_event)
            cv.waitKey(500)
        kamera.release()
        cv.destroyAllWindows()


    #selected = True
    #image = cv.imread('Lenna.png', 1)
    #while selected:
    #    cv.imshow('image', image)
    #    cv.setMouseCallback('image', click_event)
    #    cv.waitKey(500)
    #cv.destroyAllWindows()

    #image = cv.imread('Lenna.png', 1)

    #doloci barvo koze
    kamera = cv.VideoCapture(0)
    ret,image = kamera.read()
    color = doloci_barvo_koze(image, coordinates[0], coordinates[1])
    print(color)
    kamera.release()

    #image = zmanjsaj_sliko(image, 240, 320)
    #cv.imshow('image', image)
    #cv.waitKey(0)
    #cv.destroyAllWindows()

    #----------------------------

    #začne timer
    kamera = cv.VideoCapture(0)
    start_time = time.time()
    num_frames = 0

    #v zanki gledamo na kameri sliko, ki jo damo v škatle in preštejemo piksle,kože
    # tista škatla, ki ima največ preštetih pikslov in ima vsaj 50% pikslov kože glede na vseh pikslov v škatli
    # je izbrana kot škatla v kateri, bi se naj nahajal obraz
    # Prikažejo se slike sosedstvo 8, če je možno (če ni na robu slike), doda se še text za fps
    if not kamera.isOpened():
        print("Kamera ni odprta")
    else:
        while True:
            ret, image = kamera.read()
            image = zmanjsaj_sliko(image,240,320)

            imgVisina, imgSirina = image.shape[:2]
            frame_width = int(imgSirina * 0.2)
            frame_height = int(imgVisina * 0.2)

            array = obdelaj_sliko_s_skatlami(image, frame_width, frame_height, color)
            max_counter = np.max(array[:, 2])
            # print(array)

            xs, xe, ys, ye = 0,0,0,0
            counter = 0
            for x in array:
                if x[2] > int(0.5 * frame_width * frame_height) and x[2] == max_counter:

                    xs = max(0, x[0]-frame_width)
                    xe = min(imgSirina, x[0]+frame_width+frame_width)
                    ys = max(0, x[1]-frame_height)
                    ye = min(imgVisina, x[1]+frame_height +frame_height)
                    #print(xs, ys, " ", xe, ye)

                    num_frames += 1
                    elapsed_time = time.time() - start_time
                    fps = num_frames / elapsed_time

                    roi = image[ys:ye, xs:xe]
                    display_frames(roi, fps)
                    cv.imshow('roi', roi)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        kamera.release()
        cv.destroyAllWindows()
