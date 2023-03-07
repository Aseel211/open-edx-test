# Generated by Django 3.2.16 on 2022-11-03 20:07

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses_offered', models.BigIntegerField()),
                ('learners', models.BigIntegerField()),
                ('registered_learners', models.BigIntegerField()),
                ('enrollments', models.BigIntegerField()),
                ('generated_certificates', models.BigIntegerField()),
                ('extra_data', jsonfield.fields.JSONField(blank=True, default=dict, help_text='Extra information for instance data')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]