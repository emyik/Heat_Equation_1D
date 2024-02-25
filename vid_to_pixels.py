import cv2

# Function to handle mouse events for drawing a line
def draw_line(event, x, y, flags, param):
    global line_start, line_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        line_start = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            line_end = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        line_end = (x, y)
        drawing = False

# Load the video
video_path = "testing.MP4"  # Change this to your video file path
output_file = "pixel_data_along_line.txt"   # Change this to your output file path
cap = cv2.VideoCapture(video_path)

# Open the output file in write mode
with open(output_file, "w") as f_out:
    # Initialize variables for line drawing
    line_start = None
    line_end = None
    drawing = False

    # Read the first frame
    ret, frame = cap.read()

    # Create a window to draw a line
    cv2.namedWindow("Draw Line")
    cv2.setMouseCallback("Draw Line", draw_line)

    while ret:
        # Draw the line on the frame
        if line_start and line_end:
            frame_with_line = frame.copy()
            cv2.line(frame_with_line, line_start, line_end, (0, 255, 0), 2)
            cv2.imshow("Draw Line", frame_with_line)
        else:
            cv2.imshow("Draw Line", frame)

        key = cv2.waitKey(1) & 0xFF

        # If 'q' is pressed, break from the loop
        if key == ord("q"):
            break

        # If 'c' is pressed, proceed with pixel extraction along the line
        elif key == ord("c") and line_start and line_end:
            # Calculate the parameters of the line equation (y = mx + b)
            m = (line_end[1] - line_start[1]) / (line_end[0] - line_start[0])
            b = line_start[1] - m * line_start[0]

            # Extract pixel colors along the line
            num_points = max(abs(line_end[0] - line_start[0]), abs(line_end[1] - line_start[1]))
            for i in range(num_points + 1):
                x = int(line_start[0] + i * (line_end[0] - line_start[0]) / num_points)
                y = int(m * x + b)

                # Ensure coordinates are within the frame
                if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                    # Extract RGB values of the pixel
                    pixel = frame[y, x]
                    blue = pixel[0]
                    green = pixel[1]
                    red = pixel[2]

                    # Write the RGB values to the output file
                    f_out.write(f"({x}, {y}): {red} {green} {blue}\n")

            break

        ret, frame = cap.read()

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
