import cv2
import numpy as np

original = cv2.imread("original.jpg")
duplicate = cv2.imread("escala.jpg")

# Checa si las imagenes son iguales en tamaño ->
image1 = original.shape
image2 = duplicate.shape

# compara pixel por pixel si el tamaño es igual ->
if original.shape == duplicate.shape:
    print("Las imagenes tienen el mismo tamaño")
    difference = cv2.subtract(original, duplicate)
    b, g, r = cv2.split(difference)

    print(cv2.countNonZero(b))
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("Las imagenes son iguales")
    else:
        print("las imagenes son diferentes")
        print("mostando la imagen diferente ->")
        cv2.imshow("Imagen diferente", duplicate)

    cv2.imshow("difference", difference)

cv2.imshow("Original", original)
cv2.imshow("duplicate", duplicate)
cv2.waitKey(0)
cv2.destroyAllWindows()