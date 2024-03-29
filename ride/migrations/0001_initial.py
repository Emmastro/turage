from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurageUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'M'), ('Female', 'F')], max_length=6)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('national_id', models.CharField(blank=True, max_length=10, null=True)),
                ('last_latitude', models.FloatField(blank=True, null=True)),
                ('last_longitude', models.FloatField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Abstract User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('nbr_seats', models.IntegerField()),
                ('seat_used', models.IntegerField(default=0)),
                ('plate_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_passengers', models.IntegerField(default=1)),
                ('time_requested', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_to_leave', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(default='waiting', max_length=30)),
                ('time_accepted', models.DateTimeField(blank=True, null=True)),
                ('time_cancelled', models.DateTimeField(blank=True, null=True)),
                ('time_finished', models.DateTimeField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('estimated_time', models.FloatField(blank=True, null=True)),
                ('actual_time', models.FloatField(blank=True, null=True)),
                ('distance', models.FloatField(blank=True, null=True)),
                ('matched', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('turageuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('driver_license', models.CharField(max_length=50)),
                ('direction', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Driver',
            },
            bases=('ride.turageuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('turageuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('university', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Passenger',
            },
            bases=('ride.turageuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('edges', models.ManyToManyField(blank=True, to='ride.edge')),
                ('waypoints', models.ManyToManyField(blank=True, to='ride.waypoint')),
            ],
        ),
        migrations.CreateModel(
            name='RideRequestMatched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(null=True)),
                ('time_accepted', models.DateTimeField(null=True)),
                ('time_cancelled', models.DateTimeField(null=True)),
                ('time_finished', models.DateTimeField(null=True)),
                ('matches', models.ManyToManyField(to='ride.riderequest')),
            ],
        ),
        migrations.AddField(
            model_name='riderequest',
            name='destination_waypoint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination_waypoint', to='ride.waypoint'),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='origin_waypoint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_waypoint', to='ride.waypoint'),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ride.driver'),
        ),
        migrations.AddField(
            model_name='riderequest',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride.passenger'),
        ),
    ]
