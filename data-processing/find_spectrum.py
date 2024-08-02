import cv2
import numpy as np

img = cv2.imread('spectrum.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, _ = img_rgb.shape
pixels = img_rgb.reshape((height * width, 3))

spec = dict()
i = 0
# with open("spectrum.txt", "w") as f_out:
for pixel_value in pixels:
    if i%10==0: spec[str(pixel_value[0])+" "+str(pixel_value[1])+" "+str(pixel_value[2])] = 70-(70-23)/1261*i
    i+=1

# Load data from the text file
t_x = []
data_points = []
with open('data.txt', 'r') as file:
    for line in file:
        # Split each line by ", " and convert the last three elements to integers
        data_point = list(map(int, line.strip().split(", ")[-3:]))
        data_points.append(data_point)

        data_point_1 = list(map(int, line.strip().split(", ")[0:2]))
        t_x.append(data_point_1)


# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return sum((x - y) ** 2 for x, y in zip(point1, point2)) ** 0.5

i = 0
with open("tx_bnd_dn.txt", "w") as f_out:
    # Find the dictionary key with the smallest distance to each data point
    for data_point in data_points:
        min_distance = float('inf')
        closest_key = None
        for key in spec.keys():
            # Convert key to list of integers
            key_point = list(map(int, key.split()))
            distance = calculate_distance(data_point, key_point)
            if distance < min_distance:
                min_distance = distance
                closest_key = key
        f_out.write(f"{float(t_x[i][0]/24)}, {float(t_x[i][1]/30)}, {spec[closest_key]}" + "\n")
        # print(t_x[i], spec[closest_key])
        i+=1
