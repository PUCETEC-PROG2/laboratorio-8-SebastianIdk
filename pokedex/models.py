from django.db import models

class Trainer(models.Model):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    age = models.IntegerField(default=1, null=False)
    level = models.IntegerField(default=1)
    picture = models.ImageField(upload_to='trainer_images')
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Pokemon(models.Model):
    name = models.CharField(max_length=30, null=False)
    POKEMON_TYPES = {
        ('A', 'Agua'),
        ('F', 'Fuego'),
        ('T', 'Tierra'),
        ('P', 'Planta'),
        ('E', 'Eléctrico'),
        ('L', 'Lagartija'),
    }
    type = models.CharField(max_length=30, choices=POKEMON_TYPES, null=False)
    weight = models.DecimalField(null=False, default=1, max_digits=4, decimal_places=2)
    height = models.DecimalField(null=False, default=1, max_digits=4, decimal_places=2)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pokemon_images')
    
    def __str__(self) -> str:
        return self.name
    
    def get_type_display(self):
        return dict(self.POKEMON_TYPES).get(self.type, self.type)
    
    #Para poder manejar imagenes Python requiere la libreria Pillow