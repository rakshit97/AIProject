import numpy as np
import cv2
import csv

grid = np.full((8, 8), 0, dtype=np.int)
features_list = []
features_id = []
count = 0

snap = cv2.imread("1-2-3-4-mine.png")

for i in range(76, 764-85, 86):
    for j in range(366, 1054-85, 86):
        part = snap[i:i+86, j:j+86, :]
        cv2.imshow("window", part)
        cv2.waitKey(100)
        features_list.append(part.ravel())
        features_id.append(raw_input("\nType: "))

with open('features_values.csv', 'ab') as f:
    out = csv.writer(f, delimiter=',')
    out.writerows(features_list)
with open('features_id.csv', 'ab') as f:
    outs = csv.writer(f, delimiter=',')
    outs.writerow(features_id)

# square is 86 x 86
# grid is 688 x 688
# start = (76, 366), end = (764, 1054)
