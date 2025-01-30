from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
import random

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico'
    )
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Ingrese 10 dígitos numéricos.')],
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    identification = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'Ingrese 10 dígitos numéricos.')],
        blank=True,
        null=True,
        verbose_name='Cédula'
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'identification']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return self.username

class Account(models.Model):
    ACCOUNT_TYPE = [
        ('corriente', 'Corriente'),
        ('ahorro', 'Ahorro')
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='accounts',
        verbose_name='Usuario'
    )
    account_number = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        verbose_name='Número de cuenta'
    )
    account_type = models.CharField(
        max_length=10, 
        choices=ACCOUNT_TYPE,
        verbose_name='Tipo de cuenta'
    )
    funds = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        verbose_name='Saldo'
    )

    def save(self, *args, **kwargs):
        if not self.account_number:
            while True:
                number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                if not Account.objects.filter(account_number=number).exists():
                    self.account_number = number
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_number} - {self.account_type}"

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSITO', 'Depósito'),
        ('RETIRO', 'Retiro'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('PAGO SERVICIOS BASICOS', 'Pago de servicios básicos')
    ]
    
    account = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        verbose_name='Cuenta'
    )
    transaction_type = models.CharField(
        max_length=50, 
        choices=TRANSACTION_TYPES,
        verbose_name='Tipo de transacción'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name='Monto'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora'
    )
    description = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name='Descripción'
    )
    destination = models.CharField(
        max_length=100, 
        blank=True, 
        null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.timestamp}"

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'

class Service(models.Model):
    SERVICE_TYPES = [
        ('AGUA', 'Factura de agua'),
        ('ELECTRICIDAD', 'Factura de Luz'),
    ]
    
    account = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE,
        verbose_name='Cuenta'
    )
    service_type = models.CharField(
        max_length=20, 
        choices=SERVICE_TYPES,
        verbose_name='Tipo de servicio'
    )
    bill_number = models.CharField(
        max_length=50,
        verbose_name='Número de factura'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Monto'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de pago'
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name='Pagado'
    )

    def __str__(self):
        return f"{self.service_type} payment - {self.bill_number}"

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'