from django.db import models

# Create your models here.

class Voter(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    dni = models.PositiveIntegerField(unique=True, verbose_name='DNI')
    birth_date = models.DateField(verbose_name='Fecha de Nacimiento')
    zone = models.ForeignKey('Zone', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Zona')
    voted = models.BooleanField(default=False, verbose_name='Votó?')

    def __str__(self):
        return '{} | {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Voter'
        verbose_name_plural = 'Voters'
    
    @property
    def has_voted(self):
        return self.voted


class PoliticalParty(models.Model):
    party_number = models.PositiveIntegerField(unique=True, verbose_name='Número de Partido')
    party_name = models.CharField(max_length=50, verbose_name='Nombre del Partido')
    president = models.CharField(max_length=100, verbose_name='Presidente')
    vice_president = models.CharField(max_length=100, verbose_name='Vicepresidente')
    slogan = models.CharField(max_length=100, verbose_name='Eslogan')
    votes = models.IntegerField(default=0, verbose_name='Votos')


    def __str__(self):
        return '{} | {}'.format(self.party_number, self.party_name)

    class Meta:
        verbose_name = 'Political Party'
        verbose_name_plural = 'Political Parties'

    def add_vote(self):
        self.votes += 1
        self.save()


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Provincia')

    def __str__(self):
        return '{}'.format(self.name)
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'


class Locality(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Localidad')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Provincia')

    def __str__(self):
        return '{} | {}'.format(self.name, self.province)

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'

class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Zona')
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, verbose_name='Localidad')

    def __str__(self):
        return '{} | {}'.format(self.name, self.locality)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'



class Vote(models.Model):
    class TypeVote(models.TextChoices):
        AFIRMATIVO = 'afirmativo', 'Afirmativo'
        BLANCO = 'blanco', 'En blanco'
        NULO = 'nulo', 'Nulo'
        RECURRIDO = 'recurrido', 'Recurrido'
        IMPUGNADO = 'impugnado', 'Identidad impugnada'
    
    type = models.CharField(max_length=20, choices=TypeVote.choices, default=TypeVote.AFIRMATIVO)
    political_party = models.ForeignKey('PoliticalParty', on_delete=models.SET_NULL, null=True, blank=True)
    zone = models.ForeignKey('Zone', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Zona')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} | {}'.format(self.type, self.political_party)
    
    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'


class VotingStatus(models.Model):
    close = models.BooleanField(default=False, verbose_name='Cerrado?')
    date_time_close = models.DateTimeField(null=True, blank=True, verbose_name='Fecha y hora de cierre')

    def __str__(self):
        text = 'Cerrado' if self.close else 'Abierto'
        return '{}'.format(text)
    
    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'