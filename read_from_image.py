# Tashi Sherpa
# Comp Sci IA
# Feb 25 2021
import cv2
import pytesseract

#GetImage Class
#Used to open window and get camera feed
#waits for spacebar and esc to be pressed
class GetImage:

    #constructor method
    #pre: the GetImage class is called
    #post: sets up a window, showing the user what their webcam sees.
    def __init__(self):
        self.image = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cv2.namedWindow("Capture Card")
        self.images = []

    #waits for inputs, then acts on said inputs
    #pre: the webcam window is opened
    #post: all of the inputs are handled and the window is closed
    def run_capture(self):
        img_counter = 0
        while True:
            ret, frame = self.image.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Capture Card", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                self.images.append("card_picture_{}.png".format(img_counter))
                cv2.imwrite(self.images[-1], frame)
                print("{} written!".format(self.images[-1]))
                img_counter += 1

        self.image.release()
        self.close()

    #closes the webcam window
    #pre: the webcam window is opened
    #post: the webcam window is closed
    def close(self):
        cv2.destroyAllWindows()

#ReadImage Class
#uses pytesseract to read the image taken
class ReadImage:

    #constructor method
    #pre: the ReadImage class is called
    #post: an image is read
    def __init__(self, image):
        self.image = cv2.imread(image)
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        print("reading . . .")
        self.text = pytesseract.image_to_string(img_rgb)

    #returns text read
    #pre: the image is already read
    #post: returns the text that was read
    def get_text(self):
        return self.text