# Generated by Django 4.0.1 on 2022-02-01 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_perfil_foto'),
        ('instagram', '0004_remove_comentario_likes_alter_comentario_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.perfil'),
        ),
    ]