# Generated by Django 3.1.7 on 2021-05-09 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_auto_20210505_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='second_name',
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TextField(choices=[('8', '8.00'), ('83', '8.30'), ('9', '9.00'), ('93', '9.30'), ('10', '10.00'), ('1030', '10.30'), ('11', '11.00'), ('113', '11.30'), ('12', '12.00'), ('123', '12.30'), ('13', '13.00'), ('133', '13.30')])),
                ('results', models.TextField(max_length=500)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.employee')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.patient')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.treatment')),
            ],
        ),
    ]
