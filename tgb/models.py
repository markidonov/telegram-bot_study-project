from django.db import models


class Client(models.Model):
    tg_id = models.PositiveIntegerField(
        verbose_name='Телеграм id пользователя')
    name = models.CharField(max_length=150,
                            verbose_name='Имя пользователя')

    class Meta:
        verbose_name = 'Пользователь ТГ'
        verbose_name_plural = 'Пользователи ТГ'
    
    def __str__(self):
        return self.name


class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, 
                               related_name='messages')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время получения')
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text


class Order(models.Model):
    command = models.CharField(max_length=50,
                               verbose_name='Имя команды')
    answer= models.TextField(verbose_name='Ответ бота')
    
    class Meta:
        verbose_name = 'Команда для бота'
        verbose_name_plural = 'Команды для бота'
    
    def __str__(self):
        return f'Команда:{self.command} - Ответ:{self.answer}'