from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    #Afficher
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'role',
        'is_staff'
    )

     #Modifier
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Informations Personnalisées',
            {
                'fields': (
                    'role',
                    'telephone',
                    'ville',
                    'specialty',
                ),
            },
        ),
    )
        #Create
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Informations Personnalisées',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'role',        
                    'telephone',  
                    'ville',       
                    'specialty',     
                ),
            },
        ),
    )


    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'ville')


admin.site.register(User, CustomUserAdmin)