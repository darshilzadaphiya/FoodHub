from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_price', 'item_image']
        widgets = {
            'item_name': forms.TextInput(attrs={'placeholder': 'e.g Margheritta Pizza', "required":True}),
            'item_desc': forms.TextInput(attrs={'placeholder': 'e.g Fresh and Cheesy', "required":True}),
            'item_price': forms.NumberInput(attrs={'placeholder': 'e.g 10.99', "required":True}),
            'item_image': forms.URLInput(attrs={"required":False}),
        }
    def clean_item_price(self):
        price = self.cleaned_data['item_price']
        if price < 0:
            raise forms.ValidationError("Item price cannot be negative")
        return price

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get('item_name')
        desc = cleaned.get('item_desc')
        if name and desc and name.lower() in desc.lower():
            self.add_error('item_desc', "Description should add new info beyond")
        return cleaned