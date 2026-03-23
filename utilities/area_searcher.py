import mss
import numpy as np
import cv2


class AreaSearcher:

    WHITE = 200

    def __init__(self):
        self.corner = None
        self._screen_width = None
        self._screen_height = None
        self.box_dim = None

    def take_screenshot(self):
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(sct.monitors[0]))
            self._screen_width = screenshot.shape[1]
            self._screen_height = screenshot.shape[0]
            return screenshot

    def _is_white(self, pixel, threshold=WHITE):
        r, g, b = pixel[:3]
        return r > threshold and g > threshold and b > threshold

    def get_corner(self):
        if self.corner is not None:
            return self.corner
        
        screenshot = self.take_screenshot()

        height, width = screenshot.shape[:2]
        center_x = width // 2
        center_y = height // 2
        
        # Buscar hacia la derecha desde el centro hasta encontrar primer blanco
        search_x = None
        for x in range(center_x, width):
            if self._is_white(screenshot[center_y, x]):
                # Saltar esta línea blanca hasta que deje de ser blanca
                for x1 in range(x, width):
                    if not self._is_white(screenshot[center_y, x1]):
                        break
                
                # Desde aquí buscar el siguiente blanco
                for x2 in range(x1, width):
                    if self._is_white(screenshot[center_y, x2]):
                        search_x = x2
                        break
                break

        if search_x is None:
            raise RuntimeError("No se encontró el borde izquierdo del recuadro NEXT")

        # Buscar desde arriba hacia abajo sobre search_x hasta encontrar píxel blanco
        search_y = None
        for y in range(center_y):
            if self._is_white(screenshot[y, search_x]):
                search_y = y + 1
                break

        if search_y is None:
            raise RuntimeError("No se encontró el borde superior del recuadro NEXT")

        self.corner = (search_x, search_y)
        return self.corner

    def get_box_dim(self):
        if self.box_dim is not None:
            return self.box_dim

        screenshot = self.take_screenshot()

        if self.corner is None:
            self.get_corner()

        x_cr, y_cr = self.corner
        height = self._screen_height
        width = self._screen_width

        # Bajar desde la esquina por el borde izquierdo hasta que deje de ser blanco
        box_height = None
        for y in range(y_cr, height):
            if not self._is_white(screenshot[y, x_cr]):
                break
        box_height = y - y_cr

        if box_height is None:
            raise RuntimeError("No se encontró el borde inferior del recuadro")

        # Ir hacia la derecha desde la esquina por el borde superior hasta que deje de ser blanco
        box_width = None
        for x in range(x_cr, width):
            if not self._is_white(screenshot[y_cr, x]):
                break
        box_width = x - x_cr

        if box_width is None:
            raise RuntimeError("No se encontró el borde derecho del recuadro")

        self.box_dim = (box_width, box_height)
        return self.box_dim
    
    def grab_from_corner(self, corner=None, width=None, height=None):
        if corner is None:
            corner = self.corner
        if corner is None:
            raise RuntimeError("No hay esquina definida, ejecuta get_corner() primero")

        x, y = corner

        # Si no se especifican dimensiones, tomar el máximo disponible
        if self._screen_width is None or self._screen_height is None:
            self.take_screenshot()

        if width is None:
            width = self.box_dim[0]
        if height is None:
            height = self.box_dim[1]

        with mss.mss() as sct:
            region = {"left": x, "top": y, "width": width, "height": height}
            return np.array(sct.grab(region))

    def preview(self, image=None, window_name="Preview"):
        if image is None:
            image = self.grab_from_corner()

        # mss devuelve BGRA, convertir a BGR para OpenCV
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, image=None, path="capture.png"):
        if image is None:
            image = self.grab_from_corner()

        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        cv2.imwrite(path, image)
        print(f"Saved to {path}")
