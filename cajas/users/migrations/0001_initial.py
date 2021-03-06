# Generated by Django 2.0.9 on 2019-04-08 16:14

import cajas.users.models.employee
import cajas.users.models.partner
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('document_type', models.CharField(choices=[('CC', 'C??dula de ciudadania'), ('CE', 'C??dula de extranjer??a'), ('PA', 'Pasaporte')], max_length=3, verbose_name='Tipo Documento')),
                ('document_id', models.CharField(default='', max_length=15, verbose_name='N??mero Documento')),
                ('is_daily_square', models.BooleanField(default=False, verbose_name='Es cuadre diario?')),
                ('is_abstract', models.BooleanField(default=True, verbose_name='Tiene acceso a la plataforma?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Fecha')),
                ('ip', models.GenericIPAddressField(verbose_name='Direcci??n IP')),
                ('action', models.CharField(choices=[('LI', 'Inicio de sesi??n'), ('LO', 'Cierre de sesi??n')], max_length=5, verbose_name='Acci??n')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_logs', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Log de autenticaci??n',
                'verbose_name_plural': 'Logs de autenticaci??n',
            },
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Cargo',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_type', models.CharField(choices=[('FX', 'Salario Fijo'), ('PE', 'Porcentaje de comisi??n')], default='FX', max_length=2, verbose_name='Tipo de salario')),
                ('salary', models.IntegerField(default=0, verbose_name='Salario Empleado')),
                ('passport', models.FileField(blank=True, null=True, upload_to=cajas.users.models.employee.user_passport_path, verbose_name='Pasaporte')),
                ('cv', models.FileField(blank=True, null=True, upload_to=cajas.users.models.employee.user_cv_path, verbose_name='Hoja de vida')),
                ('observations', models.TextField(blank=True, help_text='Motivo para deshabilitar el empleado', null=True, verbose_name='Motivo de despido')),
                ('charge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Charge', verbose_name='Cargo de empleado')),
                ('office', models.ManyToManyField(related_name='related_employees', to='office.Office', verbose_name='Oficina')),
                ('office_country', models.ManyToManyField(related_name='related_employees', to='office.OfficeCountry', verbose_name='Oficina por Pa??s')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_employee', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, null=True, verbose_name='C??digo')),
                ('partner_type', enumfields.fields.EnumField(enum=cajas.users.models.partner.PartnerType, max_length=5, verbose_name='Tipo de socio')),
                ('consecutive', models.IntegerField(default=1, verbose_name='Consecutivo Mini-Socios')),
                ('direct_partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Partner', verbose_name='Socio Directo')),
                ('office', models.ManyToManyField(related_name='partners', to='office.OfficeCountry', verbose_name='Oficina por Pa??s')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Socio',
                'verbose_name_plural': 'Socios',
            },
        ),
    ]
