from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

from listing.helpers import delete_realtors_data

@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    using = 'users'
    list_display = ('id', 'username', 'email',)
    list_display_links = ('id', 'username', 'email',)
    list_filter = ('email',)
    search_fields = ('username', 'email')
    list_per_page = 25
       
    
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj, form, change):
        email = obj.email
        obj.delete(using=self.using)
        delete_realtors_data(email)
        
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
