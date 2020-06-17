# from django import forms
# from .models import SparePart
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
#
#
# class SparePartForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(SparePartForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_class = 'form-horizontal'
#         self.helper.form_class = 'card-body'
#         # NEW:
#         self.helper.label_class = 'col-sm-4'
#         self.helper.field_class = 'col-sm-12'
#
#         self.helper.layout = Layout(
#             Field('name', css_class='input-xlarge'),
#             Field('type', css_class='input-xlarge'),
#             Field('measurement_unit', css_class='input-xlarge'),
#             Field('measurement_unit_scale', css_class='input-xlarge'),
#             Field('quantity', css_class='input-xlarge'),
#             # NEW:
#             ButtonHolder(
#                 Submit('submit', 'Submit', css_class='btn btn-primary')
#             )
#         )
#
#     class Meta:
#         model = SparePart
#         fields = ('name', 'unit', 'quantity')
