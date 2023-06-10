from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import *
from django.db import models


# Create your models here.


class Category(MPTTModel):
    title = models.CharField('عنوان دسته بندی', max_length=30)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children',
                            verbose_name='زیردسته')
    slug = models.SlugField('اسلاگ', allow_unicode=True, blank=True, null=True, unique=True)
    created_at = models.DateTimeField('تاریخ ایجاد دسته بندی', auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ ها'
        ordering = ['parent__id']


class Product(models.Model):
    id = models.CharField("کد محصول", max_length=30, unique=True, primary_key=True)
    title = models.CharField('عنوان محصول', max_length=100)
    category = models.ForeignKey(Category, related_name='categories', verbose_name='دسته بندی',
                                 on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField("کشور", max_length=50)
    description = models.TextField('توضیحات')
    price = models.PositiveIntegerField('قیمت (تومان)', default=0)
    discount = models.PositiveIntegerField('درصد تخفیف', null=True, blank=True)
    discounted_price = models.PositiveIntegerField('قیمت تخفیف خورده (تومان)', null=True, blank=True)
    weight = models.CharField("وزن", max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    sale_count = models.IntegerField("تعداد فروش", default=0)

    def __str__(self):
        return F" محصول : {self.id} - {self.title}"

    # Discount related processes
    def save(self, *args, **kwargs):
        discount, discounted_price = None, None

        try:
            discounted_price = self.price - (self.price * self.discount / 100)
            print(discounted_price, 1)
        except:
            pass

        try:
            discount = ((self.price - self.discounted_price) / self.price) * 100
            print(discount, 2)
        except:
            pass

        if discounted_price and discount:
            self.discounted_price = discounted_price
        elif discounted_price and not discount:
            self.discounted_price = discounted_price
            self.discount = self.discount
        elif discount and not discounted_price:
            self.discount = discount
            self.discounted_price = self.discounted_price
        else:
            self.discounted_price = self.price

        super().save(*args, **kwargs)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    def get_discounted_price(self):
        price = self.discounted_price
        return "{:,.0f} تومان ".format(price)

    def get_price(self):
        price = self.price
        return "{:,.0f} تومان ".format(price)

    get_price.short_description = 'قیمت'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField('تصویر محصول', upload_to='products/img/')

    def __str__(self):
        return self.picture.url

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر محصول'


class AdditionalItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_items')
    item = models.CharField('اقلام محصول', max_length=155)

    def __str__(self):
        return self.item

    class Meta:
        verbose_name_plural = 'اقلام همراه'
        verbose_name = 'اقلام محصول'


class Spec(models.Model):
    title = models.CharField('مشخصه', max_length=255, null=True, blank=True)
    value = models.CharField('مقدار مشخصه', max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE, related_name='specifications', verbose_name='محصول')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مشخصه فنی'
        verbose_name_plural = 'مشخصات فنی'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='محصول')

    def __str__(self):
        return f"{self.user.fullname} - {self.product.title}"

    class Meta:
        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'


class Comparison(models.Model):
    """
    Model to save the products user wants to compare
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="comparison", verbose_name="کاربر")
    product1 = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                 related_name="productcompare1", verbose_name="کالای اول",
                                 null=True, blank=True)
    product2 = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                 related_name="productcompare2", verbose_name="کالای دوم",
                                 null=True, blank=True)

    def __str__(self):
        return self.user.fullname


class Comment(models.Model):
    """
    Model to save user comments and replies
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول مربوطه')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,
                               verbose_name='کامنت پدر')
    body = models.TextField('متن کامنت')
    created_at = models.DateTimeField('تاریخ و زمان', auto_now_add=True)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    def __str__(self):
        return f' نظر {self.body[:30]}  توسط کاربر  {self.user.phone_number}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class DiscountCode(models.Model):
    name = models.CharField('نام کد تخفیف', max_length=30, )
    percent = models.PositiveIntegerField('درصد', default=0)
    quantity = models.PositiveIntegerField('تعداد', default=1)
    expiration = models.DateTimeField('تاریخ انقضا', null=True, blank=True)

    def is_not_expired(self):
        if self.expiration >= timezone.localtime(timezone.now()):
            return True
        else:
            return False

    def __str__(self):
        return f'{self.name} - {self.quantity}'

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'
