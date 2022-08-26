from rest_framework.generics import GenericAPIView
from django.http.response import HttpResponse


class XLSXExportMixin:
    excel_exporter_class = None
    file_name = None

    def get_file_name(self):
        return self.file_name or self.excel_exporter_class.file_name

    def get_excel_exporter(self):
        return self.excel_exporter_class()

    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        exporter = self.get_excel_exporter()
        exporter.generate(queryset)
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = f'attachment; filename="{self.get_file_name()}.xlsx"'
        exporter.save(response)
        return response


class XLSXExportView(XLSXExportMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.export(request, *args, **kwargs)
