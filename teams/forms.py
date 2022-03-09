from django import forms

from teams.models import Team


class CreateTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        managerCandidates = kwargs.pop('managerCandidates', None)
        teamCandidates = kwargs.pop('teamCandidates', None)
        super(CreateTeamForm, self).__init__(*args, **kwargs)
        self.fields['manager'] = forms.MultipleChoiceField(
            choices=tuple([(name.pk, name.get_full_name) for name in managerCandidates]))
        self.fields['users'] = forms.MultipleChoiceField(choices=tuple([(name.pk, name.get_full_name) for name in teamCandidates]))

    name = forms.CharField(label="Group name",
                           widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Group name'}))

    class Meta:
        model = Team
        fields = ['name', 'manager', 'users']
