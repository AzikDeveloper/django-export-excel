__all__ = ["Table", "Column", "TableMeta"]

from django.core.exceptions import FieldDoesNotExist

from . import colors
from .exceptions import (
    NotUniqueExcelColumnException,
    ProgrammingError,
    TableDoesNotHaveColumnException,
)
from .styles import Style


def _get_deep_attr(obj, source):
    attributes = source.split(".")
    for attr in attributes:
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    if callable(obj):
        return obj()
    return obj


class Column:
    def __init__(self, header_name=None, width=None, source=None, dehydrate=False):
        self._header_name = header_name
        self.width = width * 100
        self.source = source
        self.table = None
        self.column_name = None
        self.context = None
        self.dehydrate = dehydrate

    def setup(self, table, column_name, context=None):
        self.context = context
        self.table = table
        self.column_name = column_name

        # set up header name
        if self._header_name is None:
            model_attr = self.source if self.source else self.column_name
            try:
                field_verbose_name = self.table.meta.model._meta.get_field(
                    model_attr
                ).verbose_name
            except FieldDoesNotExist:
                self._header_name = str(self.column_name).capitalize()
            else:
                self._header_name = str(field_verbose_name).capitalize()

        # set up model attr
        if self.source is None:
            self.source = self.column_name

    @property
    def header_name(self):
        if self._header_name is None:
            raise ProgrammingError(
                "header_name not set. most likely you forgot to call column.setup()"
            )
        return self._header_name

    def to_representation(self, obj):
        if self.dehydrate:
            value = getattr(self.table, f"get_{self.column_name}")(obj)
        else:
            value = _get_deep_attr(obj, self.source)

        if value is None:
            return self.table.meta.none_text
        return value


class TableMeta:
    model = None
    header_style = Style(
        bold=True,
        font_size=20,
        height=50,
        background_color=colors.SEA_GREEN,
        font_color=colors.WHITE,
    )
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
            raise Exception(f"_meta is not allowed in {self.__class__}")
        self.meta = self._get_meta()
        self.columns = {}

        if len(set(self.meta.columns)) != len(self.meta.columns):
            raise NotUniqueExcelColumnException(
                f"Column names must be unique in {self.__class__}"
            )

        for column in self.meta.columns:
            if hasattr(self, column):
                column_instance = getattr(self, column)
                column_instance.setup(self, column)
                self.columns[column] = column_instance
            else:
                raise TableDoesNotHaveColumnException(
                    f"Column {column} not found in {self.__class__}"
                )
