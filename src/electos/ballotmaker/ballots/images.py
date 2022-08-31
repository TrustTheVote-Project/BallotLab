# images.py
# work with images, including embedding images into
# Paragraph flowables
from electos.ballotmaker.ballots.files import FileTools

# from reportlab.platypus import Image
from reportlab.lib import utils

PROJECT_NAME = "ballotlab"


class EmbeddedImage:
    """
    EmbeddedImage creates a text string with
    markup to add to a Paragraph flowable
    """

    def __init__(self, image_name, new_width=240) -> None:
        self.image_name = image_name
        self.new_width = new_width
        self.rel_img_path = "assets/img"
        self.embed_text = ""

        image_file = FileTools(self.image_name, self.rel_img_path)
        self.file_check(image_file)
        # retrieve the image and measure it
        self.image_full_path = image_file.abs_path_to_file
        img = utils.ImageReader(self.image_full_path)
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)
        # resize based on the new width
        self.new_height = round(new_width * aspect)
        self.embed_text = f'<para leading="{round(self.new_height / 1.9)}" spaceBefore="6" spaceAfter="12"><br /><img src="{self.image_full_path}" width="{round(new_width)}" height="{self.new_height}" valign="middle"/></para>'

    def file_check(self, image_file):
        if image_file.file_found is False:
            file_error = (
                f"File {self.image_name} not found in {self.rel_img_path}"
            )
            raise FileNotFoundError(file_error)


if __name__ == "__main__":
    embed_img = EmbeddedImage("filled_bubble.png")
    print(embed_img.embed_text)
    # not_an_img = EmbeddedImage("fake_file.png")
