__all__ = ['Table', 'Column', 'TableMeta']

from django.core.exceptions import FieldDoesNotExist
from .styles import Style
from . import colors
from .exceptions import NotUniqueExcelColumnException, TableDoesNotHaveColumnException, ProgrammingError


class Column:
    def __init__(self, header_name=None, width=None, attr=None):
        self._header_name = header_name
        self.width = width * 100
        self.attr = attr
        self.table_meta = None
        self.column_name = None
        self.context = None

    def setup(self, table_meta, column_name, context=None):
        self.context = context
        self.table_meta = table_meta
        self.column_name = column_name

        # set up header name
        if self._header_name is None:
            model_attr = self.attr if self.attr else self.column_name
            try:
                field_verbose_name = self.table_meta.model._meta.get_field(model_attr).verbose_name
            except FieldDoesNotExist:
                self._header_name = str(self.column_name).capitalize()
            else:
                self._header_name = str(field_verbose_name).capitalize()

        # set up model attr
        if self.attr is None:
            self.attr = self.column_name

    @property
    def header_name(self):
        if self._header_name is None:
            raise ProgrammingError("header_name not set. most likely you forgot to call column.setup()")
        return self._header_name

    def to_representation(self, obj):
        value = getattr(obj, self.attr)
        if value is None:
            return self.table_meta.none_text
        return value


class TableMeta:
    model = None
    header_style = Style(bold=True, font_size=20, height=50, background_color=colors.SEA_GREEN,
                         font_color=colors.WHITE)
    row_style = Style(bold=False, font_size=20, height=20)
    none_text = "-"
    columns = None

    def __init__(self):
        if self.columns is None:
            self.columns = []


class Table:

    def _get_meta(self):
        if hasattr(self, "Meta"):
            meta = getattr(self, "Meta")
            return meta()
        return TableMeta()

    def __init__(self, context=None):
        self.context = context if context is not None else {}

        if hasattr(self, "_meta"):
            raise Exception("_meta is not allowed in Table")
        self.meta = self._get_meta()
        self.columns = {}

        if len(set(self.meta.columns)) != len(self.meta.columns):
            raise NotUniqueExcelColumnException("Column names must be unique in Table")

        for column in self.meta.columns:
            if hasattr(self, column):
                column_instance = getattr(self, column)
                column_instance.setup(self.meta, column)
                self.columns[column] = column_instance
            else:
                raise TableDoesNotHaveColumnException(f"Column {column} not found in Table")
