__all__ = [
    "NotUniqueExcelColumnException",
    "TableDoesNotHaveColumnException",
    "ProgrammingError",
]


class NotUniqueExcelColumnException(Exception):
    pass


class TableDoesNotHaveColumnException(Exception):
    pass


class ProgrammingError(Exception):
    pass
