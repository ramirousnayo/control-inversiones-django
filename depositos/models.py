from django.db import models

class Banco(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class DepositoPlazo(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    numero_operacion = models.CharField(max_length=50)

    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()

    capital = models.DecimalField(max_digits=15, decimal_places=2)
    tasa_anual = models.DecimalField(max_digits=5, decimal_places=2)

    def dias_inversion(self):
        return (self.fecha_vencimiento - self.fecha_inicio).days

    def interes_ganado(self):
        dias = self.dias_inversion()
        return (self.capital * (self.tasa_anual / 100) * dias) / 360

    def monto_final(self):
        return self.capital + self.interes_ganado()

    def __str__(self):
        return f"DAP {self.numero_operacion}"
