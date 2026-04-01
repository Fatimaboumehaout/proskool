from django.contrib import admin
from .models import Subject, SubjectGroup, SubjectPrerequisite

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code_unique', 'nom', 'code', 'departement', 'credits', 'heures_semaine', 'type_matiere', 'is_active')
    list_filter = ('departement', 'code', 'type_matiere', 'is_active')
    search_fields = ('nom', 'code_unique', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('code_unique', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'code', 'code_unique', 'description')
        }),
        ('Paramètres académiques', {
            'fields': ('credits', 'heures_semaine', 'type_matiere')
        }),
        ('Relations', {
            'fields': ('departement', 'enseignants')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('enseignants',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('departement')

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('subject', 'groupe', 'enseignant_principal', 'get_heures_effectives', 'get_credits_effectifs', 'is_active')
    list_filter = ('subject__departement', 'is_active')
    search_fields = ('subject__nom', 'groupe__nom')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Association', {
            'fields': ('subject', 'groupe', 'enseignant_principal')
        }),
        ('Paramètres spécifiques', {
            'fields': ('heures_specifiques', 'credits_specifiques'),
            'description': 'Laissez vide pour utiliser les valeurs par défaut de la matière'
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_heures_effectives(self, obj):
        return obj.get_heures_effectives()
    get_heures_effectives.short_description = 'Heures effectives'
    
    def get_credits_effectifs(self, obj):
        return obj.get_credits_effectifs()
    get_credits_effectifs.short_description = 'Crédits effectifs'

@admin.register(SubjectPrerequisite)
class SubjectPrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'prerequisite', 'niveau_requis')
    list_filter = ('subject__departement',)
    search_fields = ('subject__nom', 'prerequisite__nom')
    
    fieldsets = (
        ('Prérequis', {
            'fields': ('subject', 'prerequisite')
        }),
        ('Détails', {
            'fields': ('niveau_requis', 'description')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('subject', 'prerequisite', 'subject__departement')
