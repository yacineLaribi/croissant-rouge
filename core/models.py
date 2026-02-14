from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    organisations = [
        ('croissant-rouge', 'Croissant Rouge / الهلال الأحمر'),
        ('kafil-el-yatim', 'Kafil El Yatim / كافل اليتيم'),
        ('elbaraka', 'Association El Baraka / جمعية البركة'),
        # ('rabitat-oran', 'رابطة الجمعيات الفاعلة لولاية وهران / Ligue des associations actives de la wilaya d’Oran'),
        ('rabitat-oran', 'رابطة الجمعيات الفاعلة لولاية وهران'),
        ('other', 'Autre / أخرى'),
    ]

    # override username (keep it but disable usage)
    username = models.CharField(max_length=255, blank=True, null=True, unique=False)

    phone = models.IntegerField(blank=True,null=True)

    email = models.EmailField(unique=True)

    fullname = models.CharField(max_length=255, blank=True)
    organisation = models.CharField(max_length=20, choices=organisations)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # IMPORTANT

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Distribution(models.Model):
    AID_CHOICES = [
        ("colis-alimentaire", "Colis alimentaire"),
        ("aide-financiere", "Aide financière"),
        ("vetements", "Vêtements"),
        ("produits-hygiene", "Produits d'hygiène"),
        ("medicaments", "Médicaments"),
        ("autre", "Autre"),
    ]

    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    commune = models.CharField(max_length=100, blank=True)

    nin = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        unique=False,
        help_text="Numéro d'identité nationale (18 chiffres)"
    )

    ccp_or_passport = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="CCP ou autre identifiant si pas de NIN"
    )

    aid_type = models.CharField(max_length=30, choices=AID_CHOICES)
    distribution_date = models.DateField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} - {self.aid_type} ({self.distribution_date})"
