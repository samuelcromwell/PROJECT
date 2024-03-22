import os
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Event
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.units import inch
from django.conf import settings
from datetime import datetime

class StartDateListFilter(admin.DateFieldListFilter):
    title = _('Start Date')  # Custom title for the filter

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.links += (
            (_('Next 1 Week'), {
                self.lookup_kwarg_since: timezone.now().date(),
                self.lookup_kwarg_until: timezone.now().date() + timezone.timedelta(days=7),
            }),
            (_('Next 2 Weeks'), {
                self.lookup_kwarg_since: timezone.now().date(),
                self.lookup_kwarg_until: timezone.now().date() + timezone.timedelta(days=14),
            }),
            (_('Next 1 Month'), {
                self.lookup_kwarg_since: timezone.now().date(),
                self.lookup_kwarg_until: timezone.now().date() + timezone.timedelta(days=30),
            }),
            # Add more options for additional weeks if needed
        )

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start', 'end', 'instructor')
    list_filter = [
        ('start', StartDateListFilter),  # Use the custom StartDateListFilter
        ('instructor', admin.RelatedOnlyFieldListFilter),  # Add 'instructor' field to list filter
        'name',
    ]
    # search_fields = ('name',)
    # actions = [export_to_pdf]

    def export_to_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="events.pdf"'

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
        heading = Paragraph("<b>Lessons Report</b>", getSampleStyleSheet()['Heading1'])
        elements.append(heading)

        # Add space before the table
        elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

        # Table data
        data = [['Name', 'Start', 'End', 'Instructor']]
        for event in queryset:
            data.append([event.name, event.start, event.end, event.instructor])

        # Calculate column widths
        name_width = 2 * inch  # Double the default width for the 'Name' column
        start_width = 3 * inch  # Increase the width for 'Start' and 'End' columns
        instructor_width = 1 * inch  # Reduce the width for the 'Instructor' column

        # Table data
        data = [['Name', 'Date', 'Instructor']]
        for event in queryset:
            data.append([event.name, event.start, event.instructor])

        # Create a table with specified column widths
        table = Table(data, colWidths=[name_width, start_width, instructor_width])

        # Add style to the table
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "instructor":
            kwargs["queryset"] = User.objects.filter(groups__name='Instructor')  # Filter users by group membership
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return False  # Disable the "Add event" button

admin.site.register(Event, EventAdmin)
