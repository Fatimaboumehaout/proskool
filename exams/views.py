from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Avg, Max, Min
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import csv

from .models import ExamType, Exam, ExamResult, ExamSession, ExamStatistics
from .forms import ExamForm, ExamResultForm, ExamSessionForm, ExamTypeForm

# Vues pour les Examens
class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtres
        status = self.request.GET.get('status')
        exam_type = self.request.GET.get('exam_type')
        subject = self.request.GET.get('subject')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        search = self.request.GET.get('search')
        
        if status:
            queryset = queryset.filter(status=status)
        if exam_type:
            queryset = queryset.filter(exam_type_id=exam_type)
        if subject:
            queryset = queryset.filter(subject_id=subject)
        if date_from:
            queryset = queryset.filter(exam_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(exam_date__lte=date_to)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(subject__nom__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.select_related('exam_type', 'subject', 'room').prefetch_related('groups', 'teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'exam_types': ExamType.objects.all(),
            'subjects': self.get_queryset().values('subject__id', 'subject__nom').distinct(),
            'total_exams': Exam.objects.count(),
            'upcoming_exams': Exam.objects.filter(
                exam_date__gte=timezone.now().date(),
                status='planned'
            ).count(),
            'ongoing_exams': Exam.objects.filter(status='ongoing').count(),
        })
        return context

class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'
    context_object_name = 'exam'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = self.get_object()
        
        # Statistiques
        context.update({
            'results': exam.results.select_related('student').order_by('student__last_name'),
            'statistics': getattr(exam, 'statistics', None),
            'total_students': exam.get_total_students(),
            'submitted_count': exam.get_submitted_count(),
            'average_score': exam.get_average_score(),
            'success_rate': exam.get_success_rate(),
        })
        
        return context

class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exams:exam_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Examen créé avec succès!')
        return super().form_valid(form)

class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exams:exam_list')

    def form_valid(self, form):
        messages.success(self.request, 'Examen mis à jour avec succès!')
        return super().form_valid(form)

class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/exam_confirm_delete.html'
    success_url = reverse_lazy('exams:exam_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Examen supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

# Vues pour les Résultats
class ExamResultListView(LoginRequiredMixin, ListView):
    model = ExamResult
    template_name = 'exams/result_list.html'
    context_object_name = 'results'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        exam_id = self.request.GET.get('exam')
        status = self.request.GET.get('status')
        grade = self.request.GET.get('grade')
        search = self.request.GET.get('search')
        
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        if status:
            queryset = queryset.filter(status=status)
        if grade:
            queryset = queryset.filter(grade=grade)
        if search:
            queryset = queryset.filter(
                Q(student__first_name__icontains=search) | 
                Q(student__last_name__icontains=search)
            )
        
        return queryset.select_related('exam', 'student').order_by('-exam__exam_date', 'student__last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'exams': Exam.objects.all(),
            'total_results': ExamResult.objects.count(),
            'graded_results': ExamResult.objects.filter(status='graded').count(),
        })
        return context

class ExamResultCreateView(LoginRequiredMixin, CreateView):
    model = ExamResult
    form_class = ExamResultForm
    template_name = 'exams/result_form.html'
    success_url = reverse_lazy('exams:result_list')

    def form_valid(self, form):
        form.instance.graded_by = self.request.user
        messages.success(self.request, 'Résultat enregistré avec succès!')
        return super().form_valid(form)

class ExamResultUpdateView(LoginRequiredMixin, UpdateView):
    model = ExamResult
    form_class = ExamResultForm
    template_name = 'exams/result_form.html'
    success_url = reverse_lazy('exams:result_list')

    def form_valid(self, form):
        form.instance.graded_by = self.request.user
        messages.success(self.request, 'Résultat mis à jour avec succès!')
        return super().form_valid(form)

# Vues pour les Sessions d'examens
class ExamSessionListView(LoginRequiredMixin, ListView):
    model = ExamSession
    template_name = 'exams/session_list.html'
    context_object_name = 'sessions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_sessions'] = ExamSession.objects.filter(is_active=True).count()
        return context

class ExamSessionCreateView(LoginRequiredMixin, CreateView):
    model = ExamSession
    form_class = ExamSessionForm
    template_name = 'exams/session_form.html'
    success_url = reverse_lazy('exams:session_list')

    def form_valid(self, form):
        messages.success(self.request, 'Session d\'examen créée avec succès!')
        return super().form_valid(form)

# Vue Dashboard
class ExamDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'exams/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques générales
        context.update({
            'total_exams': Exam.objects.count(),
            'total_results': ExamResult.objects.count(),
            'total_sessions': ExamSession.objects.count(),
            'upcoming_exams': Exam.objects.filter(
                exam_date__gte=timezone.now().date(),
                status='planned'
            ).count(),
        })
        
        # Examens récents
        context['recent_exams'] = Exam.objects.order_by('-exam_date')[:5]
        
        # Examens en cours
        context['ongoing_exams'] = Exam.objects.filter(status='ongoing')[:5]
        
        # Statistiques par type
        exam_type_stats = Exam.objects.values('exam_type__name').annotate(
            count=Count('id'),
            avg_score=Avg('results__score')
        ).order_by('-count')
        context['exam_type_stats'] = exam_type_stats
        
        # Sessions actives
        context['active_sessions'] = ExamSession.objects.filter(is_active=True)
        
        return context

# Vue pour la notation en masse
class BulkGradingView(LoginRequiredMixin, TemplateView):
    template_name = 'exams/bulk_grading.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.request.GET.get('exam')
        
        if exam_id:
            exam = get_object_or_404(Exam, pk=exam_id)
            context['exam'] = exam
            context['students'] = exam.get_all_students()
            context['results'] = exam.results.select_related('student').order_by('student__last_name')
        
        context['exams'] = Exam.objects.filter(status__in=['ongoing', 'completed'])
        return context

    def post(self, request, *args, **kwargs):
        exam_id = request.POST.get('exam')
        exam = get_object_or_404(Exam, pk=exam_id)
        
        # Traitement des notes en masse
        for student_id, score in request.POST.items():
            if student_id.startswith('score_') and score:
                student_id = student_id.replace('score_', '')
                try:
                    result = ExamResult.objects.get(exam=exam, student_id=student_id)
                    result.score = float(score)
                    result.status = 'graded'
                    result.graded_by = request.user
                    result.save()
                except ExamResult.DoesNotExist:
                    # Créer le résultat s'il n'existe pas
                    pass
        
        messages.success(request, 'Notes enregistrées avec succès!')
        return redirect('exams:exam_detail', pk=exam_id)

# Export des résultats
def export_exam_results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="results_{exam.title}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Étudiant', 'Note', 'Note Max', 'Pourcentage', 'Appréciation', 'Statut'])
    
    for result in exam.results.select_related('student').order_by('student__last_name'):
        writer.writerow([
            f"{result.student.first_name} {result.student.last_name}",
            result.score or 'Absent',
            result.max_score,
            f"{result.get_percentage()}%" if result.get_percentage() > 0 else '-',
            result.grade or '-',
            result.get_status_display()
        ])
    
    return response

# API pour les requêtes AJAX
def exam_search_api(request):
    """API pour la recherche d'examens via AJAX"""
    query = request.GET.get('q', '')
    exams = Exam.objects.filter(
        Q(title__icontains=query) | Q(subject__nom__icontains=query)
    ).select_related('subject', 'exam_type')[:10]
    
    data = []
    for exam in exams:
        data.append({
            'id': exam.id,
            'title': exam.title,
            'subject': exam.subject.nom,
            'exam_type': exam.exam_type.name,
            'exam_date': exam.exam_date.strftime('%Y-%m-%d'),
            'status': exam.status,
        })
    
    return JsonResponse({'exams': data})
