import cv2

# DICTIONARY OF RGB -> TEMP
# img = cv2.imread('spectrum.jpg')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# height, width, _ = img_rgb.shape
# pixels = img_rgb.reshape((height * width, 3))
# spec = dict()
# i = 0
# with open("spectrum.txt", "w") as f_out:
#     for pixel_value in pixels:
#         if i%10==0: spec[str(pixel_value[0])+" "+str(pixel_value[1])+" "+str(pixel_value[2])] = 70-(70-23)/1261*i
#         i+=1

# Function to handle mouse events for drawing a line
def draw_line(event, x, y, flags, param):
    global line_start, line_end, drawing, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        line_start = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            frame = frame_copy.copy()
            cv2.line(frame, line_start, (x, y), (0, 255, 0), 2)
            cv2.imshow("Video", frame)

    elif event == cv2.EVENT_LBUTTONUP:
        line_end = (x, y)
        drawing = False
        frame = frame_copy.copy()
        cv2.line(frame, line_start, line_end, (0, 255, 0), 2)
        cv2.imshow("Video", frame)


# Load the video
video_path = "vid.mov"  # Change this to your video file path
output_file = "data.txt"   # Change this to your output file path
cap = cv2.VideoCapture(video_path)

# Read the first frame
ret, frame = cap.read()
frame_copy = frame.copy()

# Create a window to display the video
cv2.namedWindow("Video")
cv2.imshow("Video", frame)
cv2.setMouseCallback("Video", draw_line)

# Initialize variables for line drawing
line_start = None
line_end = None
drawing = False

# Wait for user to draw the line
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("c") and line_start and line_end:
        break
    elif key == ord("q"):
        cv2.destroyAllWindows()
        cap.release()
        exit()

# Create a new window to display the video
cv2.destroyAllWindows()
cv2.namedWindow("Video")

# Open the output file in write mode
with open(output_file, "w") as f_out:
    # Calculate the parameters of the line equation (y = mx + b)
    m = (line_end[1] - line_start[1]) / (line_end[0] - line_start[0])
    b = line_start[1] - m * line_start[0]

    # print("hello")
    # print(m, b)

    # Start processing the video
    frame_index = -10000
    # f_out.write("t, x, R, G, B")
    while ret:
        # CHANGING FRAMES
        target_frame_index = int(frame_index + 10000)
        # if target_frame_index == 720: break
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_index)
        ret, frame = cap.read()

        if not ret: break

        num_points = max(abs(line_end[0] - line_start[0]), abs(line_end[1] - line_start[1]))
        print(num_points)
        # CHANGING POSITION
        i = 0
        for i in range(num_points + 1):
            # if i == 720: break
            # if i%30 == 0:
            x = int(line_start[0] + i * (line_end[0] - line_start[0]) / num_points)
            y = int(m * x + b)

            if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                pixel = frame[y, x]
                blue = pixel[0]
                green = pixel[1]
                red = pixel[2]

                # Write the RGB values to the output file
                f_out.write(f"{target_frame_index}, {i}, {red}, {green}, {blue}\n")

        # Update the frame index
        frame_index = target_frame_index

        cv2.imshow("Video", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()