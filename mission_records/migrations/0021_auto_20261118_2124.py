from django.db import migrations

def set_default_fuel_type(apps, schema_editor):
    MissionFuelRefill = apps.get_model('mission_records', 'MissionFuelRefill')
    MissionFuelRefill.objects.filter(fuel_type__isnull=True).update(fuel_type='Diesel')

class Migration(migrations.Migration):
    dependencies = [
        ('mission_records', '0020_alter_missionfuelrefill_fuel_type'),
    ]

    operations = [
        migrations.RunPython(set_default_fuel_type),
    ]