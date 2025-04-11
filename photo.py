from PIL import Image, ImageEnhance


class PhotoClient:
    @staticmethod
    def process_photo(input_path, output_path):
        img = Image.open(input_path)
        img = img.convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(1.2)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
        img.save(output_path)
