from django import forms
from django.contrib import admin
from django_admin_json_editor import JSONEditorWidget
from .models import *
from import_export.admin import ImportExportModelAdmin
from . import models

# Schema for json field in products. For json editor.
DATA_SCHEMA = {
    'type': 'object',
    'title': 'Data',
    'properties': {
    },
}

class JSONModelAdminForm(forms.ModelForm):
    """ Class form for json editor """
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'characteristics': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
        }

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Registers Category model to admin """

    list_display = ['category_name', 'category_slug']
    prepopulated_fields = {'category_slug': ('category_name', )}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Registers Product model to admin """

    list_display = ['product_name', 'product_slug', 'product_price', 'product_is_aviable', 'product_created', 'product_updated', 'product_image']
    list_filter = ['product_category', 'product_is_aviable', 'product_created', 'product_updated']
    list_editable = ['product_price', 'product_is_aviable']
    prepopulated_fields = {'product_slug': ('product_name',)}
    form = JSONModelAdminForm
    search_fields = ['product_name', 'product_description']
    inlines = [ProductStockInline]
    date_hierarchy = 'product_created'

    @admin.display(description='Category')
    def category_name(self, obj):
        return obj.product_category.category_name

@admin.register(ProductReview)
class ReviewAdmin(admin.ModelAdmin):
    """ Registers Review model to admin """

    list_display = ['product', 'author', 'date_published']
    list_filter = ['product', 'date_published']

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    """ Registers UserInfo model to admin """

    list_display = ['user', 'purchased_items']


class ProductStockForm(forms.ModelForm):
    """ Custom form for ProductStock """
    class Meta:
        model = ProductStock
        fields = '__all__'


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    pass
    


class ProductForm(forms.ModelForm):
    stocks = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Stocks', is_stacked=False),
        required=False,
        label='Stocks'
    )

    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['stock_name', 'stock_slug']
    inlines = [ProductStockInline]
    list_filter = ['products']
    form = ProductForm
    filter_horizontal = ('products',)
    readonly_fields = ('get_stock_names',)
    prepopulated_fields = {'stock_slug': ('stock_name',)}
    raw_id_fields = ('products',)  # Добавлен фильтр raw_id_fields

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "products":
            kwargs["queryset"] = Product.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        products = form.cleaned_data.get('products')
        if products is not None:
            for product in products:
                ProductStock.objects.update_or_create(
                    stock=obj,
                    product=product,
                )

    def get_stock_names(self, obj):
        return ', '.join([str(product) for product in obj.products.all()])
    get_stock_names.short_description = 'Products'

class ProductExport(ImportExportModelAdmin, admin.ModelAdmin):
    ...     


from import_export.admin import ExportActionModelAdmin, ImportExportMixin
# Проверка пользователя на статус superuser
class ProductExport(ImportExportMixin, admin.ModelAdmin):
    def has_import_permission(self, request):
        if request.user.is_superuser:
            return True
        return False
    

from import_export.admin import ExportActionModelAdmin
from .models import Product

# Экспорт действий админа
class CustomExportActionModelAdmin(ExportActionModelAdmin):
    def export_custom_action(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        for Product in queryset:
            writer.writerow([obj.field1, obj.field2, obj.field3])

        return response
    export_custom_action.short_description = "Export Custom Action"
    actions = [export_custom_action]

admin.site.unregister(models.Product)
admin.site.register(models.Product, ProductExport)