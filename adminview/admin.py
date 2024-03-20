from django.contrib import admin
from django.http import HttpResponse
from .models import TraineePayment
from .forms import PaymentForm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.units import inch
from datetime import datetime
from django.conf import settings
import os
from django.db import models  # Import models module    
from django.db.models import OuterRef, Subquery, Min, Sum, Value as V
from django.db.models.functions import Coalesce
from django.db.models import F


class BalanceFilter(admin.SimpleListFilter):
    title = 'Balance'
    parameter_name = 'balance'

    def lookups(self, request, model_admin):
        return (
            ('not_zero', 'Trainees with Balances'),
            ('zero', '0 Balance (Fully Paid)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'zero':
            return queryset.annotate(
                total_balance=Coalesce(Sum('balance'), V(0), output_field=models.DecimalField())
            ).filter(total_balance=0)
        
        elif self.value() == 'not_zero':
            # Subquery to get the minimum balance for each trainee
            min_balance_subquery = TraineePayment.objects.filter(
                trainee_id=OuterRef('trainee_id')
            ).values('trainee_id').annotate(
                min_balance=Min('balance')
            ).values('min_balance')

            # Filter the queryset to include only records with positive balance and the minimum balance for each trainee
            queryset = queryset.annotate(
                min_balance=Subquery(min_balance_subquery)
            ).filter(
                balance__gt=0,
                balance=F('min_balance')
            )

            return queryset

        return queryset


class TraineePaymentAdmin(admin.ModelAdmin):
    list_display = ('username', 'amount_paid', 'balance', 'payment_date')
    list_filter = ('trainee', BalanceFilter, 'payment_date')
    

    def username(self, obj):
        return obj.trainee.username
    
    def balance(self, obj):
        return obj.balance  # Assuming balance is already calculated and stored in the TraineePayment model

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions['export_to_pdf'] = (
            self.export_to_pdf,
            'export_to_pdf',
            "Export selected payments to PDF",
        )
        return actions
    
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        total_collected = TraineePayment.objects.aggregate(total_amount=Sum('amount_paid'))['total_amount'] or 0
        extra_context['total_money_collected'] = total_collected
        return super().changelist_view(request, extra_context=extra_context)


    def export_to_pdf(self, modeladmin, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="trainee_payments.pdf"'

        # Calculate total money collected
        total_collected = queryset.aggregate(total_amount=Sum('amount_paid'))['total_amount'] or 0

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
        heading = Paragraph("<b>Payment Report</b>", getSampleStyleSheet()['Heading1'])
        elements.append(heading)
        
        # Add total money collected at the top
        total_text = Paragraph(f"<b>Total Money Collected:</b> Kshs {total_collected}", getSampleStyleSheet()['Normal'])
        elements.append(total_text)

        # Add space before the table
        elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

        # Table data
        data = [['Trainee', 'Amount Paid', 'Balance', 'Payment Date']]
        for payment in queryset:
            data.append([payment.trainee.username, payment.amount_paid, payment.balance, payment.payment_date])

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


    export_to_pdf.short_description = "Export selected payments to PDF"

admin.site.register(TraineePayment, TraineePaymentAdmin)
