import numpy as np
import cv2
import pickle

grid = np.full((8, 8), 0, dtype=np.int)
f = open('model.txt', 'rb')
s = f.read()
classifier = pickle.loads(s)

snap = cv2.imread("1-2-3-4-mine.png")
count = 0

for i in range(76, 764-85, 86):
    for j in range(366, 1054-85, 86):
        part = snap[i:i+86, j:j+86, :]
        prediction = classifier.predict(part.ravel())[0]
        if prediction == 'mine' or prediction == 'flag' or prediction == 'dead' or prediction == '1' or prediction == '2' or prediction == '3' or prediction == '4' or prediction == 'open' or prediction == 'notopen':
            count += 1
        else:
            print prediction
        cv2.imshow("window", part)
        # print prediction
        cv2.waitKey(1)

print count
# square is 86 x 86
# grid is 688 x 688
# start = (76, 366), end = (764, 1054)
