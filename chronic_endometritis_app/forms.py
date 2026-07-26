from django import forms


class MLModelForm(forms.Form):
    # Labels are set/overridden client-side by the RU/EN language switcher
    # in main.html (it matches inputs by their auto-generated id, e.g.
    # "id_FSH"), so the label text below is only the initial/fallback value.
    label_suffix = ''

    # FSH (от 0.1 до 16.4)
    FSH = forms.FloatField(
        label='FSH, mIU/l', min_value=0.1, max_value=16.4, required=True,
        widget=forms.NumberInput(attrs={
            'step': 'any', 'class': 'field-input', 'placeholder': '0.1–16.4',
        }),
    )

    # SHBG (от 21.7 до 375.2)
    SHBG = forms.FloatField(
        label='SHBG, nmol/l', min_value=21.7, max_value=375.2, required=True,
        widget=forms.NumberInput(attrs={
            'step': 'any', 'class': 'field-input', 'placeholder': '21.7–375.2',
        }),
    )

    # endometr_thick (от 3 до 14)
    endometr_thick = forms.IntegerField(
        label='Endometrial thickness, mm', min_value=3, max_value=14, required=True,
        widget=forms.NumberInput(attrs={
            'class': 'field-input', 'placeholder': '3–14',
        }),
    )

    # CRP (от 0.1 до 13.1)
    CRP = forms.FloatField(
        label='CRP, IU/L', min_value=0.1, max_value=13.1, required=True,
        widget=forms.NumberInput(attrs={
            'step': 'any', 'class': 'field-input', 'placeholder': '0.1–13.1',
        }),
    )

    # LEP_ADIPOQ (от 0.04 до 15.07)
    LEP_ADIPOQ = forms.FloatField(
        label='Leptin/adiponectin', min_value=0.04, max_value=15.07, required=True,
        widget=forms.NumberInput(attrs={
            'step': 'any', 'class': 'field-input', 'placeholder': '0.04–15.07',
        }),
    )
