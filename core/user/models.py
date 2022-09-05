from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL

# Create your models here.


class User(AbstractUser):

    turno_choices = (
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde'),
    )

    image = models.ImageField(
        upload_to="users/%y/%m/%d", null=True, blank=True)
    telefono = models.CharField(null=True, blank=True, max_length=20)
    rut = models.CharField('Rut', max_length=10, null=True, blank=True)
    turno = models.CharField('Turno', max_length=50, choices=turno_choices, null=True, blank=True)

    class Meta:
        """Meta definition for Estacionamiento."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    def __str__(self):
        return self.get_full_name()

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, "img/empty.png")

    def toJSON(self):
        item = model_to_dict(
            self, exclude=["user_permissions", "last_login"])
        if self.last_login:
            item['last_login'] = self.last_login.strftime("%Y-%m-%d")
        item['date_joined'] = self.date_joined.strftime("%Y-%m-%d")
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{"id": g.id, "name": g.name}
                          for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if "group" not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
