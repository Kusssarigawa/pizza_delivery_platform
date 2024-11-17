
# forms.py
from django import forms
from .models import Order, DeliveryLocation

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'delivery_type', 'comment','pickup_location',
                  'address',
                #   'delivery_address'
                  ]

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш адрес'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            # 'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш адрес'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(CheckoutForm, self).__init__(*args, **kwargs)
    #     self.fields['pickup_location'] = DeliveryLocation.objects.all()

# class OrderForm(forms.ModelForm):
#     confirm_phone = forms.CharField(
#         max_length=17,
#         required=True,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         label='Подтвердите телефон'
#     )

#     class Meta:
#         model = Order
#         fields = [
#             'first_name', 'last_name', 'phone', 'confirm_phone',
#             'email', 'delivery_type', 'address', 'pickup_location'
#         ]
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'delivery_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
#             'address': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3,
#                 'placeholder': 'Укажите адрес доставки'
#             }),
#             'pickup_location': forms.Select(attrs={'class': 'form-select'})
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Делаем поле address необязательным по умолчанию
#         self.fields['address'].required = False
#         self.fields['pickup_location'].required = False

#     def clean(self):
#         cleaned_data = super().clean()
#         delivery_type = cleaned_data.get('delivery_type')
#         address = cleaned_data.get('address')
#         pickup_location = cleaned_data.get('pickup_location')
#         phone = cleaned_data.get('phone')
#         confirm_phone = cleaned_data.get('confirm_phone')

#         # Проверка соответствия телефонов
#         if phone != confirm_phone:
#             raise ValidationError('Номера телефонов не совпадают')

#         # Проверка заполнения адреса или точки самовывоза
#         if delivery_type == 'delivery' and not address:
#             self.add_error('address', 'При доставке необходимо указать адрес')
#         elif delivery_type == 'pickup' and not pickup_location:
#             self.add_error('pickup_location', 'При самовывозе необходимо выбрать точку получения')

#         return cleaned_data

# class CartItemUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CartItem
#         fields = ['quantity']
#         widgets = {
#             'quantity': forms.NumberInput(attrs={
#                 'class': 'form-control form-control-sm',
#                 'min': '1',
#                 'max': '10'
#             })
#         }

# class ContactForm(forms.Form):
#     name = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Ваше имя'
#         })
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Email'
#         })
#     )
#     message = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'rows': 4,
#             'placeholder': 'Ваше сообщение'
#         })
#     )