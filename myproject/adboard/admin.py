from django.contrib import admin
from .models import Author, Ad, Response


class AuthorAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Author._meta.get_fields()]  # все поля (!Проблема итерабильности модели)
    list_display = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name', 'surname', 'sex',
                    'last_login', 'auth_code', 'b_day', 'm_mailing', 'view_my_info')
    list_filter = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name', 'surname', 'sex',
                   'last_login', 'auth_code', 'b_day', 'm_mailing', 'view_my_info')
    # а также list_editable = и куча других
    search_fields = ('username', 'email', )  # 'category__name'
    fields = ['username', 'email', 'first_name', 'last_name', 'surname', 'sex', 'b_day', 'is_active', 'is_staff',
              'auth_code', 'm_mailing', 'view_my_info']  # установить порядок полей!


class AdAdmin(admin.ModelAdmin):
    # Отображение в админке
    list_display = ('author', 'title', 'category', 'creation_date', 'last_edit_date', 'view_counter')  #'reply_counter')
    # при создании через админку (кроме полей устанавливаемых автоматически!) (ну и тех что по морально-этическим...)
    list_filter = ('author', 'title', 'category', 'creation_date', 'last_edit_date', 'view_counter')
    fields = ['author', 'title', 'category', 'text']
    # search_fields = ('__all__',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Response)
