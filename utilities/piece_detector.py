from cv2 import cvtColor, COLOR_BGRA2BGR, COLOR_BGR2HSV
class PieceDetector:

    def __init__(self):
        self.tolerance = 4
        self.colors = {
            'red' : 356,
            'yellow' : 48,
            'orange' : 23,
            'blue' : 250,
            'green' : 83,
            'turquoise' : 158,
            'rose' : 305
        }

    def _convert_to_hsv(self, image):
        bgr = cvtColor(image, COLOR_BGRA2BGR)
        return cvtColor(bgr, COLOR_BGR2HSV)
    
    def look4color(self, h):

        for color, hue in self.colors.items():
            center = hue / 2  # convertir 0-360 → 0-180
            if abs(h - center) <= self.tolerance:
                return color
        return None


    def detect(self, image, dims):
        hsv_img = self._convert_to_hsv(image)

        x_center = dims[0]//2

        is_in_piece = False

        detections = []

        for y in range(dims[1]):
            
            h = int(hsv_img[y, x_center, 0])

            if (not is_in_piece and h == 0) or is_in_piece and h != 0:
                pass

            elif not is_in_piece and h != 0:
                is_in_piece = True
                color = self.look4color(h)
                detections.append(color)

            elif is_in_piece and h == 0:
                is_in_piece = False
            
            if len(detections) == 5:
                break
        
        return detections
