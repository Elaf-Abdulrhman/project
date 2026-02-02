from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_alter_bookmark_unique_together'),
        ('posts', '0004_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('user', 'post')},
        ),
    ]
