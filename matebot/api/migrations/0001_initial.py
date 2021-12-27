# Generated by Django 4.0 on 2021-12-27 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumableMessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PollModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('balance', models.IntegerField(default=0)),
                ('permission', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('external', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('voucher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('reason', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_receiver', to='api.usermodel')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_sender', to='api.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('reason', models.CharField(blank=True, default='', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.usermodel')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.pollmodel')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.transactionmodel')),
            ],
        ),
        migrations.CreateModel(
            name='MultiTransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('transactions', models.ManyToManyField(to='api.TransactionModel')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('price', models.IntegerField()),
                ('symbol', models.CharField(max_length=15)),
                ('messages', models.ManyToManyField(blank=True, to='api.ConsumableMessageModel')),
            ],
        ),
        migrations.CreateModel(
            name='CommunismUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='CommunismModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('amount', models.IntegerField()),
                ('reason', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('accessed', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.usermodel')),
                ('participants', models.ManyToManyField(blank=True, to='api.CommunismUserModel')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationCallbackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserAliasModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_user_id', models.CharField(max_length=255, unique=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.application')),
            ],
        ),
        migrations.CreateModel(
            name='VoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.usermodel')),
                ('vote', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='pollmodel',
            name='votes',
            field=models.ManyToManyField(blank=True, to='api.VoteModel'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='user_aliases',
            field=models.ManyToManyField(to='api.UserAliasModel'),
        ),
    ]