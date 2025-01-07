__all__ = ["Style"]

from functools import cached_property

import xlwt

from . import colors


class Style:
    def __init__(
        self,
        bold=False,
        italic=False,
        underline=False,
        font_color=colors.BLACK,
        font_size=None,
        background_color=colors.WHITE,
        rotate_90=False,
        height=None,
        xlwt_style=None,
        center_text=True,
    ):

        self.background_color = background_color
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.font_size = font_size * 10
        self.font_color = font_color
        self.rotate_90 = rotate_90
        self.height = height * 10
        self._xlwt_style = xlwt_style
        self.center_text = center_text

    @cached_property
    def xlw_style(self):
        if self._xlwt_style:
            return self._xlwt_style

        style = xlwt.XFStyle()
        style.font.bold = self.bold
        style.font.italic = self.italic
        style.font.underline = self.underline
        style.font.height = self.font_size
        style.font.colour_index = self.font_color

        style.borders.top = xlwt.Borders.THIN
        style.borders.bottom = xlwt.Borders.THIN
        style.borders.right = xlwt.Borders.THIN
        style.borders.left = xlwt.Borders.THIN

        if self.center_text:
            style.alignment.horz = xlwt.Alignment.HORZ_CENTER
            style.alignment.vert = xlwt.Alignment.VERT_CENTER

        if self.rotate_90:
            style.alignment.rota = 90

        style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        style.pattern.pattern_fore_colour = self.background_color

        return style
