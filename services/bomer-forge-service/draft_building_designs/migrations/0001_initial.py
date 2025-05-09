# Generated by Django 5.1.6 on 2025-03-15 12:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('building_components', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftBuildingDesign',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phase', models.CharField(choices=[('PHASE_1', 'Phase 1'), ('PHASE_2', 'Phase 2'), ('PHASE_3', 'Phase 3')], default='PHASE_1', max_length=255)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='DRAFT', max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='draft_building_designs', to='projects.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DraftBuildingDesignBuildingComponent',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('justification', models.TextField(default='')),
                ('task_id', models.CharField(blank=True, max_length=255, null=True)),
                ('bom', models.JSONField(blank=True, null=True)),
                ('building_component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='building_components.buildingcomponent')),
                ('draft_building_design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='draft_building_designs.draftbuildingdesign')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='draftbuildingdesign',
            name='building_components',
            field=models.ManyToManyField(related_name='draft_building_designs', through='draft_building_designs.DraftBuildingDesignBuildingComponent', to='building_components.buildingcomponent'),
        ),
    ]
