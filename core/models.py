from django.db import models

class CorpoCeleste(models.Model):
    CATEGORIAS = (
        ('estrela', 'Estrela'),
        ('planeta', 'Planeta'),
        ('lua', 'Lua'),
    )

    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    tipo = models.CharField(max_length=100, blank=True)
    distancia = models.CharField(max_length=100, blank=True)
    diametro = models.CharField(max_length=100, blank=True)
    massa = models.CharField(max_length=100, blank=True)
    temperatura = models.CharField(max_length=100, blank=True)
    composicao = models.TextField(blank=True)
    curiosidades = models.TextField()
    foto = models.ImageField(upload_to='corpos_celestes/', null=True, blank=True)

    planeta_pai = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='luas'
    )

    def __str__(self):
        return self.nome
# Create your models here.
