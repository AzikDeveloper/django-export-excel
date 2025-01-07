__all__ = ["ModelExcelExporter"]

import xlwt
from django.utils.translation import gettext as _g
from django.utils.translation import gettext_lazy as _

from .table import Table


class Counter:
    def __init__(self, start):
        self.start = start
        self.counter = start

    def add(self, delta):
        self.counter += delta
        return self.counter


class ModelExcelExporter:
    table_class = None
    file_name = "results"
    sheet_name = _g("main")
    style_compression = 1
    include_row_number = False

    def __init__(self, context=None, sheet_name=None, file_name=None):
        if context is None:
            self.context = {}
        if sheet_name is not None:
            self.sheet_name = sheet_name

        if file_name is not None:
            self.file_name = file_name

        assert (
                self.table_class is not None
        ), f"{self.__class__}.table_class must be set"

        self._wb = xlwt.Workbook(self.style_compression)
        self._ws = self._wb.add_sheet(str(self.sheet_name))
        self._table = self.table_class(context=self.context)

    def generate(self, queryset):
        Ex = Counter(0)
        Ey = Counter(2)

        if self.include_row_number:
            self._put_cell(
                (Ex.counter, Ey.counter),
                (Ex.add(1), Ey.counter + 1),
                self._table.meta.header_style.xlw_style,
                str(_("Number")),
            )

        # headers
        self._ws.row(Ey.counter).height_mismatch = True
        self._ws.row(Ey.counter).height = self._table.meta.header_style.height

        for column_name, column in self._table.columns.items():
            self._put_cell(
                (Ex.counter, Ey.counter),
                (Ex.add(1), Ey.counter + 1),
                self._table.meta.header_style.xlw_style,
                text=str(column.header_name),
            )
        Ex.counter = 0
        Ey.add(1)

        # data
        for i, obj in enumerate(queryset, start=1):
            if self.include_row_number:
                self._put_cell(
                    (Ex.counter, Ey.counter),
                    (Ex.add(1), Ey.counter + 1),
                    self._table.meta.row_style.xlw_style,
                    text=i,
                )

            for column_name, column in self._table.columns.items():
                self._ws.col(Ex.counter).width = column.width
                self._put_cell(
                    (Ex.counter, Ey.counter),
                    (Ex.add(1), Ey.counter + 1),
                    self._table.meta.row_style.xlw_style,
                    text=str(column.to_representation(obj)),
                )
            Ey.add(1)
            Ex.counter = 0

    def _put_cell(self, start, end, style, text):
        self._ws.write_merge(
            start[1], end[1] - 1, start[0], end[0] - 1, text, style
        )

    def save(self, stream_or_name=None):
        if stream_or_name is None:
            stream_or_name = f"{self.file_name}.xls"
        return self._wb.save(stream_or_name)
