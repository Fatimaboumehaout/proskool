from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from .models import Subject, SubjectGroup, SubjectPrerequisite
from .forms import SubjectForm, SubjectGroupForm, SubjectPrerequisiteForm

# Vues pour les Matières
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtres
        departement_id = self.request.GET.get('departement')
        code = self.request.GET.get('code')
        search = self.request.GET.get('search')
        
        if departement_id:
            queryset = queryset.filter(departement_id=departement_id)
        if code:
            queryset = queryset.filter(code=code)
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) | 
                Q(description__icontains=search) |
                Q(code_unique__icontains=search)
            )
        
        return queryset.select_related('departement').prefetch_related('enseignants')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'departements': Subject.objects.values_list('departement__id', 'departement__name').distinct(),
            'codes': Subject.CODE_CHOICES,
            'total_subjects': Subject.objects.count(),
            'total_credits': Subject.objects.aggregate(total=Sum('credits'))['total'] or 0,
        })
        return context

class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject
    template_name = 'subjects/subject_detail.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        context.update({
            'subject_groups': SubjectGroup.objects.filter(subject=subject).select_related('groupe', 'enseignant_principal'),
            'prerequisites': SubjectPrerequisite.objects.filter(subject=subject).select_related('prerequisite'),
            'prerequisite_for': SubjectPrerequisite.objects.filter(prerequisite=subject).select_related('subject'),
            'total_heures': subject.get_total_heures(),
            'enseignants_count': subject.get_enseignants_count(),
        })
        return context

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Matière créée avec succès!')
        return super().form_valid(form)

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, 'Matière mise à jour avec succès!')
        return super().form_valid(form)

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    success_url = reverse_lazy('subjects:subject_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Matière supprimée avec succès!')
        return super().delete(request, *args, **kwargs)

# Vues pour les SubjectGroup (matières par groupe)
class SubjectGroupListView(LoginRequiredMixin, ListView):
    model = SubjectGroup
    template_name = 'subjects/subjectgroup_list.html'
    context_object_name = 'subject_groups'
    paginate_by = 10

    def get_queryset(self):
        return SubjectGroup.objects.select_related('subject', 'groupe', 'enseignant_principal').order_by('subject__code_unique', 'groupe__nom')

class SubjectGroupCreateView(LoginRequiredMixin, CreateView):
    model = SubjectGroup
    form_class = SubjectGroupForm
    template_name = 'subjects/subjectgroup_form.html'
    success_url = reverse_lazy('subjects:subjectgroup_list')

    def form_valid(self, form):
        messages.success(self.request, 'Association matière-groupe créée avec succès!')
        return super().form_valid(form)

class SubjectGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = SubjectGroup
    form_class = SubjectGroupForm
    template_name = 'subjects/subjectgroup_form.html'
    success_url = reverse_lazy('subjects:subjectgroup_list')

    def form_valid(self, form):
        messages.success(self.request, 'Association matière-groupe mise à jour avec succès!')
        return super().form_valid(form)

class SubjectGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = SubjectGroup
    template_name = 'subjects/subjectgroup_confirm_delete.html'
    success_url = reverse_lazy('subjects:subjectgroup_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Association matière-groupe supprimée avec succès!')
        return super().delete(request, *args, **kwargs)

# Vue dashboard
class SubjectDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'subjects/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques générales
        context.update({
            'total_subjects': Subject.objects.count(),
            'total_subject_groups': SubjectGroup.objects.count(),
            'total_prerequisites': SubjectPrerequisite.objects.count(),
            'total_credits': Subject.objects.aggregate(total=Sum('credits'))['total'] or 0,
            'total_heures': Subject.objects.aggregate(total=Sum('heures_semaine'))['total'] or 0,
        })
        
        # Statistiques par département
        dept_stats = Subject.objects.values('departement__name').annotate(
            count=Count('id'),
            credits=Sum('credits'),
            hours=Sum('heures_semaine')
        ).order_by('-count')
        context['department_stats'] = dept_stats
        
        # Matières récentes
        context['recent_subjects'] = Subject.objects.order_by('-created_at')[:5]
        
        # Matières sans enseignants
        context['subjects_without_teachers'] = Subject.objects.filter(enseignants__isnull=True)[:5]
        
        return context

# API pour les requêtes AJAX
def subject_search_api(request):
    """API pour la recherche de matières via AJAX"""
    query = request.GET.get('q', '')
    subjects = Subject.objects.filter(
        Q(nom__icontains=query) | Q(code_unique__icontains=query)
    ).select_related('departement')[:10]
    
    data = []
    for subject in subjects:
        data.append({
            'id': subject.id,
            'code_unique': subject.code_unique,
            'nom': subject.nom,
            'departement': subject.departement.name,
            'credits': subject.credits,
            'heures_semaine': subject.heures_semaine,
        })
    
    return JsonResponse({'subjects': data})
