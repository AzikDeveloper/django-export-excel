__all__ = ["ExportActionMixin"]

from django.http.response import HttpResponse
from django.utils.translation import gettext_lazy as _


class ExportActionMixin:
    def __new__(cls, *args, **kwargs):
        assert cls.excel_exporter_class is not None, (
            "You must define a excel_exporter_class or get_excel_exporter "
            "method in {}".format(cls.__name__)
        )
        return super().__new__(cls)

    excel_exporter_class = None

    def get_actions(self, request):
        """
        Adds the export action to the list of available actions.
        """

        actions = super().get_actions(request)
        actions.update(
            admin_export_to_excel_action=(
                ExportActionMixin.admin_export_to_excel_action,
                "admin_export_to_excel_action",
                _("Export selected %(verbose_name_plural)s to Excel"),
            )
        )
        return actions

    def get_excel_exporter(self):
        return self.excel_exporter_class()

    def admin_export_to_excel_action(self, request, queryset):
        exporter = self.get_excel_exporter()
        exporter.generate(queryset)
        response = HttpResponse(content_type="application/ms-excel")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{exporter.file_name}.xls"'
        exporter.save(response)
        return response
