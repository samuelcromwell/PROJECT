from django.contrib import admin
from django.http import HttpResponse
from .models import TraineePayment
from .forms import PaymentForm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class TraineePaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('username', 'amount_paid', 'balance', 'payment_date')
    list_filter = ('trainee', 'balance')  # Add trainee as a filter option

    def username(self, obj):
        return obj.trainee.username
    
    def balance(self, obj):
        return obj.balance  # Assuming balance is already calculated and stored in the TraineePayment model

    def export_to_pdf(self, modeladmin, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="trainee_payments.pdf"'

        # Create a PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Table data
        data = [['Trainee', 'Amount Paid', 'Balance']]
        for payment in queryset:
            data.append([payment.trainee.username, payment.amount_paid, payment.balance])

        # Create a table
        table = Table(data)

        # Add style to the table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)
        elements.append(table)

        # Build PDF document
        doc.build(elements)

        return response

    export_to_pdf.short_description = "Export selected payments to PDF"

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions['export_to_pdf'] = (
            self.export_to_pdf,
            'export_to_pdf',
            "Export selected payments to PDF",
        )
        return actions

admin.site.register(TraineePayment, TraineePaymentAdmin)
