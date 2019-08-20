import requests
from PIL import Image
from PIL import ImageFilter
from io import BytesIO
from rssa.utils.constants import THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH, BACKGROUND_HEIGHT, BACKGROUND_WIDTH
class Thumbnail():
    def __init__(self, image_urls):
        for url in image_urls:
            img = self.get_image_from_url(url)
            if img is not None:
                self.image = img
                break
    def get_image_from_url(self, url):
        try :
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
            return image
        except Exception as e:
            return None
    def get_blob(self):
        try:
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