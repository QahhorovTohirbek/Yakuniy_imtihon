from django.db import models
from random import sample
import string
import qrcode
from io import BytesIO
from django.core.files import File



class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(CodeGenerate):
    """ Mahsulot kategoriyasi """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(CodeGenerate):
    """ Mahsulot """
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    quantity = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def save(self, *args, **kwargs):
        QRcode = qrcode.QRCode()
        QRcode.add_data(f"Mahsulot nomi: {self.name} \n Mahsulot narxi: {self.price} so'm ")
        QRcode.make(fit=True)
        QRimg = QRcode.make_image(fill_color="black", back_color="white")
        file_name = f"qr_code {self.id}.png"
        buffer = BytesIO()
        QRimg.save(buffer, "PNG")
        self.qr_code.save(file_name, File(buffer), save=False)
        QRimg.close()
        super().save(*args, **kwargs)


        

    def __str__(self):
        return self.name
    

class Entery(CodeGenerate):
    """ Mahsulot kiritish """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.pk:
            object = Entery.objects.get(id=self.id)
            self.product.quantity -= int(object.quantity)
        
        self.product.quantity += int(self.quantity)
        self.product.save()
        super(Entery, self).save(*args, **kwargs)

    

class Outery(CodeGenerate):
    """ Mahsulot chiqish """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.pk:
            object = Outery.objects.get(id=self.id)
            self.product.quantity += int(object.quantity)

        self.product.quantity -= int(self.quantity)
        self.product.save()
        super(Outery, self).save(*args, **kwargs)


class Return(CodeGenerate):
    """ Qaytarilgan tovarlar """
    outery = models.ForeignKey(Outery, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.outery.product.name} - {self.quantity}"


    def save(self, *args, **kwargs):
        if self.pk:
            object = Return.objects.get(id=self.id)
            self.outery.product.quantity -= int(object.quantity)
            
        self.outery.product.quantity += int(self.quantity)
        self.outery.product.save()
        super(Return, self).save(*args, **kwargs)
