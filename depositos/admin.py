from django.contrib import admin
from .models import Banco, DepositoPlazo

@admin.register(DepositoPlazo)
class DepositoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_operacion',
        'banco',
        'capital',
        'tasa_anual',
        'fecha_inicio',
        'fecha_vencimiento',
        'interes_ganado',
        'monto_final',
    )
    list_filter = ('banco', 'fecha_vencimiento')
    search_fields = ('numero_operacion',)

admin.site.register(Banco)
