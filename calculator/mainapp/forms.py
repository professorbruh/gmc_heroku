from django import forms


class UpdateMarksForm(forms.Form):
    roll_number = forms.CharField()
    name = forms.CharField()
    marks = forms.IntegerField()


class EventsForm(forms.Form):
    no_of_events = forms.IntegerField()


class ModifyGradeForm(forms.Form):
    fromA = forms.IntegerField()
    toA = forms.IntegerField()
    fromB = forms.IntegerField()
    toB = forms.IntegerField()
    fromC = forms.IntegerField()
    toC = forms.IntegerField()
    fromF = forms.IntegerField()
    toF = forms.IntegerField()
    credits = forms.IntegerField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    confirm_new_password = forms.CharField
