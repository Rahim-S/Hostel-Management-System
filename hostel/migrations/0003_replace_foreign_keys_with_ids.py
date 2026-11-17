import django.db.models.deletion
from django.db import migrations, models


def copy_related_ids(apps, schema_editor):
    database = schema_editor.connection.alias
    Room = apps.get_model('hostel', 'Room')
    Student = apps.get_model('hostel', 'Student')
    Warden = apps.get_model('hostel', 'Warden')
    Payment = apps.get_model('hostel', 'Payment')

    for room in Room.objects.using(database).select_related('hostel_id').iterator():
        room.hostel_id_text = room.hostel_id.hostel_id
        room.save(using=database, update_fields=['hostel_id_text'])

    for student in Student.objects.using(database).select_related('room_id').iterator():
        student.room_id_text = student.room_id.room_id
        student.save(using=database, update_fields=['room_id_text'])

    for warden in Warden.objects.using(database).select_related('hostel_id').iterator():
        warden.hostel_id_text = warden.hostel_id.hostel_id
        warden.save(using=database, update_fields=['hostel_id_text'])

    for payment in Payment.objects.using(database).select_related('student_id').iterator():
        payment.student_id_text = payment.student_id.student_id
        payment.save(using=database, update_fields=['student_id_text'])


def restore_foreign_keys(apps, schema_editor):
    database = schema_editor.connection.alias
    Room = apps.get_model('hostel', 'Room')
    Student = apps.get_model('hostel', 'Student')
    Warden = apps.get_model('hostel', 'Warden')
    Payment = apps.get_model('hostel', 'Payment')
    related_fields = (
        (Room, 'hostel_id', 'hostel_id_text', apps.get_model('hostel', 'Hostel'), 'hostel_id'),
        (Student, 'room_id', 'room_id_text', apps.get_model('hostel', 'Room'), 'room_id'),
        (Warden, 'hostel_id', 'hostel_id_text', apps.get_model('hostel', 'Hostel'), 'hostel_id'),
        (Payment, 'student_id', 'student_id_text', apps.get_model('hostel', 'Student'), 'student_id'),
    )

    for model, relation, text_field, related_model, related_id in related_fields:
        for record in model.objects.using(database).all().iterator():
            matches = related_model.objects.using(database).filter(
                **{related_id: getattr(record, text_field)}
            )
            if matches.count() != 1:
                raise RuntimeError(
                    f'Cannot restore {model.__name__}.{relation}: '
                    f'{related_id} must match exactly one record.'
                )
            setattr(record, f'{relation}_id', matches.get().pk)
            record.save(using=database, update_fields=[relation])


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0002_alter_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='hostel_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hostel.hostel'),
        ),
        migrations.AlterField(
            model_name='student',
            name='room_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hostel.room'),
        ),
        migrations.AlterField(
            model_name='warden',
            name='hostel_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hostel.hostel'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='student_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hostel.student'),
        ),
        migrations.AddField(
            model_name='room',
            name='hostel_id_text',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='room_id_text',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='warden',
            name='hostel_id_text',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='student_id_text',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.RunPython(copy_related_ids, restore_foreign_keys),
        migrations.RemoveField(
            model_name='room',
            name='hostel_id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='room_id',
        ),
        migrations.RemoveField(
            model_name='warden',
            name='hostel_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='student_id',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='hostel_id_text',
            new_name='hostel_id',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='room_id_text',
            new_name='room_id',
        ),
        migrations.RenameField(
            model_name='warden',
            old_name='hostel_id_text',
            new_name='hostel_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='student_id_text',
            new_name='student_id',
        ),
        migrations.AlterField(
            model_name='room',
            name='hostel_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='room_id',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='warden',
            name='hostel_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='student_id',
            field=models.CharField(max_length=10),
        ),
    ]
