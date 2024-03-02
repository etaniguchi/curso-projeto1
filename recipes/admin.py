from django.contrib import admin
from .models import Category, Recipe

class CategoryAdmin(admin.ModelAdmin):
    pass

class RecipeAdmin(admin.ModelAdmin):
    # colunas visiveis da lista de receitas
    list_display = ['id','title','created_at','is_published','author']
    # colunas com links
    list_display_links = 'title','author',
    # busca por estas colunas
    search_fields = 'id','title','description','slug','preparation_steps',
    # filtro interativo
    list_filter = 'category','author','is_published',\
        'preparation_steps_is_html',
    # qtde por pagina
    list_per_page = 10
    # campo fica editavel na lista
    list_editable = 'is_published',
    # ordenação
    ordering = '-id',
    # slug fica com preenchimento automatico
    prepopulated_fields = {
        "slug": ('title',)
    }

admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)


