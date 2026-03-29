from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Tu nombre'}))
    last_name = forms.CharField(label='Apellido', max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Tu apellido'}))
    email = forms.EmailField(label='Email',
                              widget=forms.EmailInput(attrs={'placeholder': 'hola@tucorreo.com'}))
    phone = forms.CharField(label='Teléfono', max_length=20,
                             widget=forms.TextInput(attrs={'placeholder': '+57 300 000 0000'}))
    country = forms.CharField(label='País', max_length=100, initial='Colombia',
                               widget=forms.TextInput(attrs={'placeholder': 'Colombia'}))
    department = forms.CharField(label='Departamento', max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Bolívar'}))
    city = forms.CharField(label='Ciudad', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Cartagena'}))
    address = forms.CharField(label='Dirección', max_length=300,
                               widget=forms.TextInput(attrs={'placeholder': 'Calle, carrera, barrio'}))
    postal_code = forms.CharField(label='Código postal', max_length=20, required=False,
                                   widget=forms.TextInput(attrs={'placeholder': '130001'}))
    notes = forms.CharField(label='Notas del pedido', required=False,
                             widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Instrucciones especiales de entrega...'}))
