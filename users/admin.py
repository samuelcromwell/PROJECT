from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.functions import ExtractYear
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.units import inch
import os
from django.conf import settings
from datetime import datetime

class YearOfBirthFilter(admin.SimpleListFilter):
    title = _('Year of Birth')
    parameter_name = 'year_of_birth'

    def lookups(self, request, model_admin):
        years = CustomUser.objects.annotate(year=ExtractYear('date_of_birth')).values_list('year', flat=True).distinct()
        return [(year, year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date_of_birth__year=self.value())



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'date_of_birth')
    list_filter = ['groups', 'date_joined', YearOfBirthFilter]  # Include the custom YearOfBirthFilter

    def export_to_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="custom_users.pdf"'

        # Create a PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add logo at the top
        logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
        logo = Image(logo_path, width=2*inch, height=1*inch)
        elements.append(logo)

        # Add space after the logo
        elements.append(Paragraph("<br/>", getSampleStyleSheet()['Normal']))

        # Add today's date
        today = datetime.today().strftime("%Y-%m-%d")
        date_text = Paragraph(f"<b>Date:</b> {today}", getSampleStyleSheet()['Normal'])
        elements.append(date_text)

        # Add space before the heading
        elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

        # Add heading
        heading = Paragraph("<b>User Report</b>", getSampleStyleSheet()['Heading1'])
        elements.append(heading)

        # Add space before the table
        elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

        # Table data
        data = [['Username', 'Date Joined', 'Date of Birth']]
        for user in queryset:
            data.append([user.username, user.date_joined, user.date_of_birth])

        # Calculate column widths
        num_cols = len(data[0])
        table_width = letter[0] - inch * 2  # Subtracting 2 inches for left and right margins
        col_width = table_width / num_cols
        col_widths = [col_width] * num_cols

        # Create a table with specified column widths
        table = Table(data, colWidths=col_widths)

        # Add style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Body background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid color
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Box color
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),  # Inner grid color
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
            ('LEADING', (0, 0), (-1, -1), 12),  # Leading (line spacing)
            ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding
            ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Left padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),  # Right padding
        ])
        table.setStyle(style)
        elements.append(table)

        # Build PDF document
        doc.build(elements)

        return response

    export_to_pdf.short_description = _("Export selected users to PDF")

    actions = ['export_to_pdf']

admin.site.register(CustomUser, CustomUserAdmin)
