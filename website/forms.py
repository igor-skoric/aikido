from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Ime',
        widget=forms.TextInput(attrs={
            'class': 'contact-page__input',
            'placeholder': 'Vaše ime',
            'autocomplete': 'name',
        }),
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'contact-page__input',
            'placeholder': 'vas@email.com',
            'autocomplete': 'email',
        }),
    )
    message = forms.CharField(
        label='Poruka',
        widget=forms.Textarea(attrs={
            'class': 'contact-page__input contact-page__input--textarea',
            'rows': 6,
            'placeholder': 'Vaša poruka…',
        }),
    )
