import cv2

img = cv2.imread('image1.png')
blur = cv2.medianBlur(img, 5)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray,100,255, cv2.THRESH_BINARY_INV)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

dictions = {0:[575,589],
            1:[590,604],
            2:[605,619],
            3:[620,634],
            4:[635,649],
            5:[650,664],
            6:[665,679],
            7:[680,694],
            8:[695,709],
            9:[710,724],
            }


min_area = 10
black_dots = []
for c in cnts:
   area = cv2.contourArea(c)
   if area > min_area:
      M = cv2.moments(c)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      start = 122
      count = 22
      if cX == 20 and cY == 1083:
          cv2.drawContours(img, [c], -1, (36, 12, 255), 2)
      if cX == 763 and cY == 1083:
          cv2.drawContours(img, [c], -1, (36, 12, 255), 2)
      if cX == 763 and cY == 32:
          cv2.drawContours(img, [c], -1, (36, 12, 255), 2)
      if cX == 20 and cY == 32:
          cv2.drawContours(img, [c], -1, (36, 12, 255), 2)
      black_dots.append(c)

print("Black Dots Count is:",len(black_dots))

Xmax = 0
Ymax = 0
Xmin = 10000
Ymin = 10000
for c in black_dots:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print("X:",cX)
    print("Y:",cY)
    Xmax = max(Xmax, cX)
    Ymax = max(Ymax, cY)

for c in black_dots:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    Xmin = min(Xmin, cX)
    Ymin = min(Ymin, cY)

print("Xmax:",Xmax)
print("Ymax:",Ymax)
print("Xmin:",Xmin)
print("Ymin:",Ymin)

print(abs(Ymax - Xmax))

img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imshow('Output image', img)
cv2.waitKey()