
###### Pasos a seguir #######

1) Migrar tablas a la BBDD con los comando:
- python manage.py makemigrations
- python manage.py migrate

2) Restaurar database.json con el comando:
- python manage.py loaddata database.json

3) Crear super usuario con el comando:
- python manage.py createsuperuser

4) Crear grupo administrador con los siguientes permisos:
- Cliente
- Plan
- Reserva
- Tarifa
