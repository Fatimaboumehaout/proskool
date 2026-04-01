from django.contrib import admin
from .models import Salle, Enseignant, Groupe, Cours

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite', 'created_at')
    list_filter = ('capacite',)
    search_fields = ('nom', 'description')
    ordering = ('nom',)

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'specialite', 'telephone')
    list_filter = ('specialite',)
    search_fields = ('nom', 'email', 'specialite')
    ordering = ('nom',)

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'effectif', 'created_at')
    list_filter = ('niveau',)
    search_fields = ('nom', 'niveau')
    ordering = ('nom',)

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'enseignant', 'groupe', 'salle', 'jour_semaine', 'plage_horaire')
    list_filter = ('jour_semaine', 'plage_horaire', 'enseignant', 'groupe', 'salle')
    search_fields = ('nom', 'enseignant__nom', 'groupe__nom', 'salle__nom')
    ordering = ('jour_semaine', 'plage_horaire')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'couleur')
        }),
        ('Assignation', {
            'fields': ('enseignant', 'groupe', 'salle')
        }),
        ('Horaire', {
            'fields': ('jour_semaine', 'plage_horaire')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # édition
            return ()
        return ()  # création
