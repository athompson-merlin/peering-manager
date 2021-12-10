# Generated by Django 3.1.3 on 2020-12-07 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("peeringdb", "0012_peerrecord_visible")]

    def flush_peeringdb_tables(apps, schema_editor):
        apps.get_model("peeringdb", "Contact").objects.all().delete()
        apps.get_model("peeringdb", "Network").objects.all().delete()
        apps.get_model("peeringdb", "NetworkIXLAN").objects.all().delete()
        apps.get_model("peeringdb", "PeerRecord").objects.all().delete()
        apps.get_model("peeringdb", "Synchronization").objects.all().delete()

    operations = [migrations.RunPython(flush_peeringdb_tables)]
