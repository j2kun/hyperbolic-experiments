from PIL import Image
from PIL import ImageDraw


class PoincareDisk(object):

    """A class representing an instance of the Poincare disk model.

    The model consists of the interior of a unit disk in the plane. Lines are
    arcs of circles perpendicular to the boundary of the disk.
    """

    def __init__(self):
        pass

    def render_as_image(self, canvas_width=500, canvas_height=500):
        image = Image.new('RGBA', (canvas_width, canvas_height))
        draw = ImageDraw.Draw(image)
        draw.point([(250, 250)], fill="red")
        draw.ellipse([150, 150, 200, 200], fill="black")
        image.show()


if __name__ == "__main__":
    PoincareDisk().render_as_image()
