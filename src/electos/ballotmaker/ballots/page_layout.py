# page_layout.py
# Stores page layout settings in a class
# TODO: refactor as a dict or dataclass

# customize only what's different from the samples

from dataclasses import dataclass


@dataclass
class PageLayout:
    # use floats for these values
    font_family: str = "Helvetica"
    margin: float = 0.6
    col_width: float = 2.25
    col_height: float = 9.5
    col_space: float = 0.15

    # font family info
    font_normal: str = "Helvetica"
    font_bold: str = "Helvetica-Bold"
    font_size: int = 12
    normal_lead: int = 15
    head_lead: int = 20
    border_pad: int = 8
    space_before: int = 12
    space_after: int = 6

    # define CMYKColor values
    # Use floats! (0 - 1) Didn't work with values 0 - 100
    # 100% cyan
    dark: tuple = (1, 0, 0, 0)
    # light cyan
    light: tuple = (0.1, 0, 0, 0)
    white: tuple = (0, 0, 0, 0)
    black: tuple = (0, 0, 0, 1)
    grey: tuple = (0, 0, 0, 0.15)

    bg_color: tuple = white
    border_color: tuple = black
    keep_w_next = False

    # TODO: Rewrite with *args, **kwargs?
    def define_custom_style(
        style,
        bg_color=bg_color,
        border_pad=border_pad,
        font_sz=font_size,
        txt_color=black,
        font_n=font_normal,
        line_space=font_size + 1,
        sp_before=space_before,
        sp_after=space_after,
        keep_w_next=keep_w_next,
    ):
        style.backColor = bg_color
        style.borderPadding = border_pad
        style.fontSize = font_sz
        style.textColor = txt_color
        style.fontName = font_n
        style.leading = line_space
        style.spaceBefore = sp_before
        style.spaceAfter = sp_after
        style.keepWithNext = keep_w_next


if __name__ == "__main__":
    print(dir(PageLayout))
