# django-export-excel

Django package for exporting data to Excel file with included admin integration.
Note that this is not a django app.


# Usage


### Creating Table class
```
class MyModelTable(Table):
    id = Column(header_name="ID", width=20)
    name = Column(header_name="Name", width=20)
    age = Column(width=20)
    images = Column(header_name="Images", width=50, attr="get_images")

    class Meta(TableMeta):
        model = MyModel
        columns = [
            "id",
            "name",
            "age",
            "images"
        ]
        header_style = Style(bold=True, font_size=20, height=50, background_color=colors.SEA_GREEN,
                             font_color=colors.WHITE)
        row_style = Style(bold=False, font_size=20, height=20)
        none_text = "-"
```
### Creating Exporter class
```
class MyModelExcelExporter(ModelExcelExporter):
    table_class = MyModelTable
    file_name = "results"
    sheet_name = "main"
    style_compression = 2
    include_row_number = True
```

### Generating ecxel
```
exporter = MyModelExcelExporter()
exporter.generate(queryset=MyModel.objects.all())
exporter.save()
```

## Django Admin integration
Sublass from ExportActionMixin and django's ModelAdmin to add "Export to excel" action

