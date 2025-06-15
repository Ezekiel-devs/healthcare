from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 1. Champs à afficher dans la liste des utilisateurs
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'role',
        'is_staff'
    )

    # 2. Champs sur la page de MODIFICATION
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Informations Personnalisées',
            {
                'fields': (
                    'role',
                    'phone_number',
                    'telephone',
                    'ville',
                    'specialty',
                ),
            },
        ),
    )

    # 3. Champs sur la page de CRÉATION  <--- C'EST ICI QU'IL FAUT CORRIGER
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Informations Personnalisées',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'role',          # Déjà là
                    'telephone',  # ==> AJOUTER
                    'ville',       # ==> AJOUTER
                    'specialty',     # ==> AJOUTER
                ),
            },
        ),
    )

    # 4. Filtres
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    
    # 5. Recherche
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'ville')


admin.site.register(User, CustomUserAdmin)