from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg, Max, Min
from .models import ExamType, Exam, ExamResult, ExamSession, ExamStatistics

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'default_duration', 'max_score', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'start_date', 'end_date', 'get_exams_count', 'is_active')
    list_filter = ('is_active', 'academic_year')
    search_fields = ('name', 'academic_year')
    readonly_fields = ('created_at',)

    def get_exams_count(self, obj):
        count = obj.get_exams_count()
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 5px 10px; border-radius: 3px;">{}</span>',
            count
        )
    get_exams_count.short_description = "Examens"

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'exam_type', 'subject', 'exam_date', 'start_time', 
        'get_total_students', 'get_submitted_count', 'status_badge', 'is_published'
    )
    list_filter = ('status', 'exam_type', 'exam_date', 'is_published')
    search_fields = ('title', 'subject__name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'get_total_students', 'get_submitted_count', 'get_average_score', 'get_success_rate')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'exam_type', 'subject')
        }),
        ('Planification', {
            'fields': ('exam_date', 'start_time', 'duration', 'end_time', 'room')
        }),
        ('Participants', {
            'fields': ('groups', 'teachers')
        }),
        ('Paramètres', {
            'fields': ('max_score', 'passing_score', 'status', 'is_published')
        }),
        ('Statistiques', {
            'fields': ('get_total_students', 'get_submitted_count', 'get_average_score', 'get_success_rate'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('groups', 'teachers')

    def get_total_students(self, obj):
        count = obj.get_total_students()
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 5px 10px; border-radius: 3px;">{}</span>',
            count
        )
    get_total_students.short_description = "Total étudiants"

    def get_submitted_count(self, obj):
        count = obj.get_submitted_count()
        color = '#4caf50' if count > 0 else '#f44336'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, count
        )
    get_submitted_count.short_description = "Soumis"

    def get_average_score(self, obj):
        avg = obj.get_average_score()
        if avg > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                avg
            )
        return "-"
    get_average_score.short_description = "Moyenne"

    def get_success_rate(self, obj):
        rate = obj.get_success_rate()
        if rate > 0:
            color = '#4caf50' if rate >= 50 else '#ff9800'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}%</span>',
                color, rate
            )
        return "-"
    get_success_rate.short_description = "Taux réussite"

    def status_badge(self, obj):
        colors = {
            'planned': '#2196f3',
            'ongoing': '#ff9800',
            'completed': '#4caf50',
            'cancelled': '#f44336'
        }
        color = colors.get(obj.status, '#9e9e9e')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Statut"

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'exam', 'score_display', 'grade_badge', 'status_badge', 'is_passed_badge', 'graded_at'
    )
    list_filter = ('status', 'is_passed', 'grade', 'exam__exam_type', 'exam__subject')
    search_fields = ('student__first_name', 'student__last_name', 'exam__title')
    readonly_fields = ('created_at', 'updated_at', 'submitted_at', 'graded_at', 'get_percentage')
    
    fieldsets = (
        ('Informations', {
            'fields': ('exam', 'student')
        }),
        ('Notes', {
            'fields': ('score', 'max_score', 'get_percentage', 'grade', 'comment')
        }),
        ('Statut', {
            'fields': ('status', 'is_passed')
        }),
        ('Dates', {
            'fields': ('submitted_at', 'graded_at', 'graded_by')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def score_display(self, obj):
        if obj.score is not None:
            percentage = obj.get_percentage()
            color = '#4caf50' if percentage >= 50 else '#f44336'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}/{} ({:.1f}%)</span>',
                color, obj.score, obj.max_score, percentage
            )
        return "-"
    score_display.short_description = "Note"

    def grade_badge(self, obj):
        if obj.grade:
            colors = {
                'A': '#4caf50',
                'B': '#8bc34a',
                'C': '#ffeb3b',
                'D': '#ff9800',
                'E': '#ff5722',
                'F': '#f44336'
            }
            color = colors.get(obj.grade, '#9e9e9e')
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
                color, obj.grade
            )
        return "-"
    grade_badge.short_description = "Appréciation"

    def status_badge(self, obj):
        colors = {
            'absent': '#f44336',
            'submitted': '#2196f3',
            'graded': '#4caf50',
            'appealed': '#ff9800'
        }
        color = colors.get(obj.status, '#9e9e9e')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Statut"

    def is_passed_badge(self, obj):
        if obj.is_passed is True:
            return format_html(
                '<span style="background-color: #4caf50; color: white; padding: 5px 10px; border-radius: 3px;">Admis</span>'
            )
        elif obj.is_passed is False:
            return format_html(
                '<span style="background-color: #f44336; color: white; padding: 5px 10px; border-radius: 3px;">Ajourné</span>'
            )
        return "-"
    is_passed_badge.short_description = "Résultat"

    def get_percentage(self, obj):
        return f"{obj.get_percentage()}%" if obj.get_percentage() > 0 else "-"
    get_percentage.short_description = "Pourcentage"

@admin.register(ExamStatistics)
class ExamStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'exam', 'total_students', 'submitted_count', 'graded_count', 
        'average_score_display', 'success_rate_display', 'grade_distribution'
    )
    readonly_fields = ('updated_at',)
    
    def average_score_display(self, obj):
        if obj.average_score:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                obj.average_score
            )
        return "-"
    average_score_display.short_description = "Moyenne"

    def success_rate_display(self, obj):
        if obj.success_rate:
            color = '#4caf50' if obj.success_rate >= 50 else '#ff9800'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}%</span>',
                color, obj.success_rate
            )
        return "-"
    success_rate_display.short_description = "Taux réussite"

    def grade_distribution(self, obj):
        total = obj.graded_count
        if total == 0:
            return "-"
        
        distribution = []
        for grade, count in [('A', obj.a_count), ('B', obj.b_count), ('C', obj.c_count), 
                           ('D', obj.d_count), ('E', obj.e_count), ('F', obj.f_count)]:
            if count > 0:
                percentage = (count / total) * 100
                colors = {'A': '#4caf50', 'B': '#8bc34a', 'C': '#ffeb3b', 
                         'D': '#ff9800', 'E': '#ff5722', 'F': '#f44336'}
                color = colors[grade]
                distribution.append(format_html(
                    '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 2px; margin: 1px;">{}: {}%</span>',
                    color, grade, round(percentage)
                ))
        
        return format_html(' '.join(distribution))
    grade_distribution.short_description = "Distribution"
