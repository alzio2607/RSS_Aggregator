import requests
from PIL import Image
from PIL import ImageFilter
from io import BytesIO
from rssa.utils.constants import THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH, BACKGROUND_HEIGHT, BACKGROUND_WIDTH
from google_images_download import google_images_download
class Thumbnail():
    def __init__(self, image_urls, title):
        self.image = None
        for url in image_urls:
            img = self.get_image_from_url(url)
            if img is not None:
                self.image = img
                break
        if self.image is None:
            try:
                response = google_images_download.googleimagesdownload()
                arguments = {"keywords": title, "limit": 1, "print_urls": False}
                paths = response.download(arguments)
                path = paths[0][paths[0].keys()[0]][0]
                self.image = Image.open(open(path, 'rb'))
            except:
                pass


    def get_image_from_url(self, url):
        try :
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
            return image
        except Exception as e:
            return None

    def crop_to_square(self, image):
        width  = image.size[0]
        height = image.size[1]
        aspect = width / float(height)
        ideal_aspect = 1.0

        if aspect > ideal_aspect:
            # Then crop the left and right edges:
            new_width = int(ideal_aspect * height)
            offset = (width - new_width) / 2
            resize = (offset, 0, width - offset, height)
        else:
            # ... crop the top and bottom:
            new_height = int(width / ideal_aspect)
            offset = (height - new_height) / 2
            resize = (0, offset, width, height - offset)

        thumb = image.crop(resize).resize((300, 300), Image.ANTIALIAS)
        return thumb

    def get_blob(self):
        try:
            self.image = self.crop_to_square(self.image)
            stream = BytesIO()
            self.image.save(stream, format="JPEG")
            return stream.getvalue()
        except Exception as e:
            return None

    def get_background(self):
        try:
            self.bg = self.image.filter(ImageFilter.GaussianBlur(16))
            self.bg = self.bg.resize((BACKGROUND_WIDTH, BACKGROUND_HEIGHT), Image.ANTIALIAS)
            blankImage = Image.new("RGB", size=(BACKGROUND_WIDTH, BACKGROUND_HEIGHT), color='white')
            self.bg = Image.blend(blankImage, self.bg, 0.3)
            return self.bg
        except:
            return None