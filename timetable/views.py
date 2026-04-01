from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from .models import Salle, Enseignant, Groupe, Cours, JOURS_SEMAINE, PLAGES_HORAIRE
from .forms import SalleForm, EnseignantForm, GroupeForm, CoursForm, EmploiDuTempsForm

# Vues pour les Salles
class SalleListView(LoginRequiredMixin, ListView):
    model = Salle
    template_name = 'timetable/salle_list.html'
    context_object_name = 'salles'
    paginate_by = 10

class SalleCreateView(LoginRequiredMixin, CreateView):
    model = Salle
    form_class = SalleForm
    template_name = 'timetable/salle_form.html'
    success_url = reverse_lazy('timetable:salle_list')

    def form_valid(self, form):
        messages.success(self.request, 'Salle créée avec succès!')
        return super().form_valid(form)

class SalleUpdateView(LoginRequiredMixin, UpdateView):
    model = Salle
    form_class = SalleForm
    template_name = 'timetable/salle_form.html'
    success_url = reverse_lazy('timetable:salle_list')

    def form_valid(self, form):
        messages.success(self.request, 'Salle mise à jour avec succès!')
        return super().form_valid(form)

class SalleDeleteView(LoginRequiredMixin, DeleteView):
    model = Salle
    template_name = 'timetable/salle_confirm_delete.html'
    success_url = reverse_lazy('timetable:salle_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Salle supprimée avec succès!')
        return super().delete(request, *args, **kwargs)

# Vues pour les Enseignants
class EnseignantListView(LoginRequiredMixin, ListView):
    model = Enseignant
    template_name = 'timetable/enseignant_list.html'
    context_object_name = 'enseignants'
    paginate_by = 10

class EnseignantCreateView(LoginRequiredMixin, CreateView):
    model = Enseignant
    form_class = EnseignantForm
    template_name = 'timetable/enseignant_form.html'
    success_url = reverse_lazy('timetable:enseignant_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enseignant créé avec succès!')
        return super().form_valid(form)

class EnseignantUpdateView(LoginRequiredMixin, UpdateView):
    model = Enseignant
    form_class = EnseignantForm
    template_name = 'timetable/enseignant_form.html'
    success_url = reverse_lazy('timetable:enseignant_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enseignant mis à jour avec succès!')
        return super().form_valid(form)

class EnseignantDeleteView(LoginRequiredMixin, DeleteView):
    model = Enseignant
    template_name = 'timetable/enseignant_confirm_delete.html'
    success_url = reverse_lazy('timetable:enseignant_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Enseignant supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

# Vues pour les Groupes
class GroupeListView(LoginRequiredMixin, ListView):
    model = Groupe
    template_name = 'timetable/groupe_list.html'
    context_object_name = 'groupes'
    paginate_by = 10

class GroupeCreateView(LoginRequiredMixin, CreateView):
    model = Groupe
    form_class = GroupeForm
    template_name = 'timetable/groupe_form.html'
    success_url = reverse_lazy('timetable:groupe_list')

    def form_valid(self, form):
        messages.success(self.request, 'Groupe créé avec succès!')
        return super().form_valid(form)

class GroupeUpdateView(LoginRequiredMixin, UpdateView):
    model = Groupe
    form_class = GroupeForm
    template_name = 'timetable/groupe_form.html'
    success_url = reverse_lazy('timetable:groupe_list')

    def form_valid(self, form):
        messages.success(self.request, 'Groupe mis à jour avec succès!')
        return super().form_valid(form)

class GroupeDeleteView(LoginRequiredMixin, DeleteView):
    model = Groupe
    template_name = 'timetable/groupe_confirm_delete.html'
    success_url = reverse_lazy('timetable:groupe_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Groupe supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

# Vues pour les Cours
class CoursListView(LoginRequiredMixin, ListView):
    model = Cours
    template_name = 'timetable/cours_list.html'
    context_object_name = 'cours_list'
    paginate_by = 10

class CoursCreateView(LoginRequiredMixin, CreateView):
    model = Cours
    form_class = CoursForm
    template_name = 'timetable/cours_form.html'
    success_url = reverse_lazy('timetable:cours_list')

    def form_valid(self, form):
        try:
            messages.success(self.request, 'Cours créé avec succès!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Erreur: {str(e)}')
            return self.form_invalid(form)

class CoursUpdateView(LoginRequiredMixin, UpdateView):
    model = Cours
    form_class = CoursForm
    template_name = 'timetable/cours_form.html'
    success_url = reverse_lazy('timetable:cours_list')

    def form_valid(self, form):
        try:
            messages.success(self.request, 'Cours mis à jour avec succès!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Erreur: {str(e)}')
            return self.form_invalid(form)

class CoursDeleteView(LoginRequiredMixin, DeleteView):
    model = Cours
    template_name = 'timetable/cours_confirm_delete.html'
    success_url = reverse_lazy('timetable:cours_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cours supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

# Vue principale pour l'emploi du temps
class EmploiDuTempsView(LoginRequiredMixin, TemplateView):
    template_name = 'timetable/emploi_du_temps.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = EmploiDuTempsForm(self.request.GET or None)
        emploi_du_temps = None
        groupe_selectionne = None

        if form.is_valid() and form.cleaned_data.get('groupe'):
            groupe_selectionne = form.cleaned_data['groupe']
            emploi_du_temps = self.generer_emploi_du_temps(groupe_selectionne)

        context.update({
            'form': form,
            'emploi_du_temps': emploi_du_temps,
            'groupe_selectionne': groupe_selectionne,
            'jours': [jour[0] for jour in JOURS_SEMAINE],
            'plages_horaires': [plage[0] for plage in PLAGES_HORAIRE],
        })
        return context

    def generer_emploi_du_temps(self, groupe):
        """Génère l'emploi du temps sous forme de dictionnaire"""
        emploi_du_temps = {}
        
        # Initialiser la structure
        for jour in [jour[0] for jour in JOURS_SEMAINE]:
            emploi_du_temps[jour] = {}
            for plage in [plage[0] for plage in PLAGES_HORAIRE]:
                emploi_du_temps[jour][plage] = None

        # Remplir avec les cours du groupe
        cours = Cours.objects.filter(groupe=groupe).select_related('enseignant', 'salle')
        
        for cour in cours:
            emploi_du_temps[cour.jour_semaine][cour.plage_horaire] = cour

        return emploi_du_temps

# Vue dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'timetable/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_salles': Salle.objects.count(),
            'total_enseignants': Enseignant.objects.count(),
            'total_groupes': Groupe.objects.count(),
            'total_cours': Cours.objects.count(),
            'cours_recent': Cours.objects.order_by('-created_at')[:5],
        })
        return context
