from django import forms
from django.contrib.auth.models import User

from kebabs.models import Order 

# Safe from injection, etc.
class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('Delivery_time','Delivery_point','Delivery_instruction','Payment_method')
	def save(self, commit=True):
		order = super(OrderForm, self).save(commit=False)
		order.Delivery_time = self.cleaned_data['Delivery_time']
		order.Delivery_point = self.cleaned_data['Delivery_point']
		order.Delivery_instruction = self.cleaned_data['Delivery_instruction']
		order.Payment_method = self.cleaned_data['Payment_method']
		#Missing totalcost and ordercreator
		if commit:
			order.save()
		return order
