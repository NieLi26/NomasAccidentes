from email import message
from celery.schedules import crontab
from celery import Celery
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import uuid
import time

from django.template.loader import render_to_string
from config import settings
from django.core.mail import send_mail

from celery import shared_task

from notifications.signals import notify
from core.erp.models import Asesoria, AsesoriaEspecial, Capacitacion, Contrato, Empresa, Pago, Visita


from django.contrib.auth import get_user_model

User = get_user_model()

app = Celery()

########### TAREAS PERIODICAS ###########


@app.task(name="send_notification")
def send_notification():
    try:
        for i in Capacitacion.objects.all():
            po = i.fecha_realizacion
            po = po - timedelta(15)
            if po == date.today():
                recipients = User.objects.filter(id=i.cli.user.id)

                for recipient in recipients:
                    subject = 'Alerta Capacitacion'
                    message = 'Faltan 2 semanas para su capacitacion'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [recipient.email]
                    send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(e)


@app.task(name="send_email_actividad")
def send_email_actividad():
    try:
        ######################  UN DIA ANTES #####################

        # Asesoria
        if Asesoria.objects.filter(completado=False):
            for i in Asesoria.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(1)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que mañana se realizara su asesoria agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Asesoria Especial
        if AsesoriaEspecial.objects.filter(completado=False):
            for i in AsesoriaEspecial.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(1)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que mañana se realizara su asesoria especial agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Capacitacion
        if Capacitacion.objects.filter(completado=False):
            for i in Capacitacion.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(1)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que mañana se realizara su capacitacion agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Visita
        if Visita.objects.filter(completado=False):
            for i in Visita.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(1)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que mañana se realizara su visita agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Pago
        # for i in Pago.objects.all():
        #     fecha = i.fecha_expiracion
        #     resto_fecha = fecha - timedelta(15)
        #     if resto_fecha == date.today():
        #         user = User.objects.get(id=i.cli.user.id)

        #         mailServer = smtplib.SMTP(
        #             settings.EMAIL_HOST, settings.EMAIL_PORT)
        #         mailServer.starttls()
        #         mailServer.login(settings.EMAIL_HOST_USER,
        #                          settings.EMAIL_HOST_PASSWORD)

        #         email_to = user.email
        #         mensaje = MIMEMultipart()
        #         mensaje['From'] = settings.EMAIL_HOST_USER
        #         mensaje['To'] = email_to
        #         mensaje['Subject'] = 'Aviso Pago'

        #         content = render_to_string('message/send_email_pago.html', {
        #             'user': user,
        #             'emp': Empresa.objects.get(user=user),
        #             'mensaje': 'Se le recuerda que faltan solo 15 dias para que expire su fecha de pago el',
        #             'desc': i.desc,
        #             'asunto': i.asunto,
        #             'valor': i.valor,
        #             'fecha': fecha
        #         })

        #         # content = render_to_string('message/send_email.html', {
        #         #     'user': user,
        #         #     'emp': Empresa.objects.get(user=user),
        #         #     'mensaje': 'Se le recuerda que faltan solo 15 dias para que expire su fecha de pago el:',
        #         #     'desc': i.desc,
        #         #     'fecha': fecha
        #         # })
        #         mensaje.attach(MIMEText(content, 'html'))

        #         mailServer.sendmail(settings.EMAIL_HOST_USER,
        #                             email_to,
        #                             mensaje.as_string())

        # contrato
        if Contrato.objects.filter(activo=True):
            for i in Contrato.objects.all():
                fecha = i.fecha_termino
                resto_fecha = fecha - timedelta(1)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.emp.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Contrato'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que mañana se cumple el termino de su contrato el:',
                        'fecha': fecha
                    })

                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        ###################### 2 SEMANAS ANTES #####################

        # Asesoria
        if Asesoria.objects.filter(completado=False):
            for i in Asesoria.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(15)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que faltan solo 15 dias para realizar su asesoria agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Asesoria Especial
        if AsesoriaEspecial.objects.filter(completado=False):
            for i in AsesoriaEspecial.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(15)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que faltan solo 15 dias para realizar su asesoria especial agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Capacitacion
        if Capacitacion.objects.filter(completado=False):
            for i in Capacitacion.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(15)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que faltan solo 15 dias para realizar su capacitacion agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Visita
        if Visita.objects.filter(completado=False):
            for i in Visita.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha - timedelta(15)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que faltan solo 15 dias para realizar su visita agendada el:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Pago
        # for i in Pago.objects.all():
        #     fecha = i.fecha_expiracion
        #     resto_fecha = fecha - timedelta(15)
        #     if resto_fecha == date.today():
        #         user = User.objects.get(id=i.cli.user.id)

        #         mailServer = smtplib.SMTP(
        #             settings.EMAIL_HOST, settings.EMAIL_PORT)
        #         mailServer.starttls()
        #         mailServer.login(settings.EMAIL_HOST_USER,
        #                          settings.EMAIL_HOST_PASSWORD)

        #         email_to = user.email
        #         mensaje = MIMEMultipart()
        #         mensaje['From'] = settings.EMAIL_HOST_USER
        #         mensaje['To'] = email_to
        #         mensaje['Subject'] = 'Aviso Pago'

        #         content = render_to_string('message/send_email_pago.html', {
        #             'user': user,
        #             'emp': Empresa.objects.get(user=user),
        #             'mensaje': 'Se le recuerda que faltan solo 15 dias para que expire su fecha de pago el',
        #             'desc': i.desc,
        #             'asunto': i.asunto,
        #             'valor': i.valor,
        #             'fecha': fecha
        #         })

        #         # content = render_to_string('message/send_email.html', {
        #         #     'user': user,
        #         #     'emp': Empresa.objects.get(user=user),
        #         #     'mensaje': 'Se le recuerda que faltan solo 15 dias para que expire su fecha de pago el:',
        #         #     'desc': i.desc,
        #         #     'fecha': fecha
        #         # })
        #         mensaje.attach(MIMEText(content, 'html'))

        #         mailServer.sendmail(settings.EMAIL_HOST_USER,
        #                             email_to,
        #                             mensaje.as_string())

        # contrato
        if Contrato.objects.filter(activo=True):
            for i in Contrato.objects.all():
                fecha = i.fecha_termino
                resto_fecha = fecha - timedelta(15)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.emp.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Contrato'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que faltan solo 15 dias para el termino de su contrato el:',
                        'fecha': fecha
                    })

                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())


     ######################  7 DIA ATRASO #####################
     
        # Asesoria
        if Asesoria.objects.filter(completado=False):
            for i in Asesoria.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha + timedelta(7)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que ya han pasado 7 dias de la fecha agendada de su asesoria que aun no se realiza:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Asesoria Especial
        if AsesoriaEspecial.objects.filter(completado=False):
            for i in AsesoriaEspecial.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha + timedelta(7)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que ya han pasado 7 dias de la fecha agendada de su asesoria especial que aun no se realiza:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Capacitacion
        if Capacitacion.objects.filter(completado=False):
            for i in Capacitacion.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha + timedelta(7)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que ya han pasado 7 dias de la fecha agendada de su capacitacion que aun no se realiza:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())

        # Visita
        if Visita.objects.filter(completado=False):
            for i in Visita.objects.all():
                fecha = i.fecha_realizacion
                resto_fecha = fecha + timedelta(7)
                if resto_fecha == date.today():
                    user = User.objects.get(id=i.cli.user.id)

                    mailServer = smtplib.SMTP(
                        settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.starttls()
                    mailServer.login(settings.EMAIL_HOST_USER,
                                     settings.EMAIL_HOST_PASSWORD)

                    email_to = user.email
                    mensaje = MIMEMultipart()
                    mensaje['From'] = settings.EMAIL_HOST_USER
                    mensaje['To'] = email_to
                    mensaje['Subject'] = 'Aviso Actividad'

                    content = render_to_string('message/send_email.html', {
                        'user': user,
                        'emp': Empresa.objects.get(user=user),
                        'mensaje': 'Se le recuerda que ya han pasado 7 dias de la fecha agendada de su visita que aun no se realiza:',
                        'fecha': fecha
                        # 'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                        # 'link_home': 'http://{}'.format(URL)
                    })
                    mensaje.attach(MIMEText(content, 'html'))

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                        email_to,
                                        mensaje.as_string())


    except Exception as e:
        print(e)

############ TAREAS ASINCRONICAS #########

# @shared_task
# def start_running(info):
#     time.sleep(5)
#     print(info)
#     print('--- >> Iniciar tarea << ---')
#     print('Enviar mensaje de texto o correo electrónico')
#     print('> --- Fin de la tarea --- <')


# @shared_task
# def test_capacitacion(sender):
#     time.sleep(10)
#     for i in Capacitacion.objects.all():
#         po = i.fecha_realizacion
#         po = po - timedelta(15)
#         if po == date.today():
#             print('> --- Fin de la tarea --- <')
#             users = User.objects.filter(id=i.cli.user.id)
#             notify.send( actor=sender, recipient=users,
#                         verb='Alerta Capacitacion', description='Se genero una alerta de capacitacion', soft_delete=True)
