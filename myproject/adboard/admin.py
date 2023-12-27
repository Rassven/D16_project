from django.contrib import admin
from .models import Author, Ad, Response


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'last_login', 'is_active', 'is_staff', 'email',
                    # 'first_name', 'last_name', 'surname', 'sex',
                    'auth_code', 'b_day', 'm_mailing', 'view_my_info')
    # list_filter = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name', 'surname',
    #                'last_login', 'auth_code', 'b_day', 'm_mailing', )
    # search_fields = ('username', 'email', 'last_login',)
    fields = ['username', 'email', 'first_name', 'last_name', 'surname', 'sex', 'b_day', 'is_active', 'is_staff',
              'auth_code', 'm_mailing', 'view_my_info']


class AdAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'category', 'creation_date', 'last_edit_date', 'view_counter')
    list_filter = ('author', 'title', 'category', 'creation_date', 'last_edit_date', 'view_counter')
    fields = ['author', 'title', 'category', 'text']
    # search_fields = ('__all__',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Response)
