# django-export-excel

Django package for exporting data to Excel file with included admin integration.
Note that this is not a django app.

This package uses [`xlwt`](https://github.com/python-excel/xlwt). Which means max 65535 rows in a file 😌.

# Usage


### Creating Table class
```
class UserTable(Table):
    id = Column(header_name="ID", width=20)
    name = Column(header_name="Name", width=20)
    birth_date = Column(width=20)
    favorite_songs = Column(width=50, attr="get_favorite_songs")

    class Meta(TableMeta):
        model = User
        columns = [
            "id",
            "name",
            "birth_date",
            "favorite_songs"
        ]
        header_style = Style(bold=True, font_size=20, height=50, background_color=colors.SEA_GREEN,
                             font_color=colors.WHITE)
        row_style = Style(bold=False, font_size=20, height=20)
        none_text = "-"
```
### Creating Exporter class
```
class UserExcelExporter(ModelExcelExporter):
    table_class = UserTable
    file_name = "users"
    sheet_name = "main"
    style_compression = 2
    include_row_number = True
```

### Generating excel
```
exporter = UserExcelExporter()
exporter.generate(queryset=User.objects.all())
exporter.save()
```
### Result
![alt text](https://github.com/AzikDeveloper/django-export-excel/blob/master/result.png)

## Django Admin integration
1. Subclass from `ExportActionMixin` and django admin's `ModelAdmin`.
2. Define your exporter class with  `excel_exporter_class` attribute in your model admin
