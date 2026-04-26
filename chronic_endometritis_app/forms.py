from django import forms


class MLModelForm(forms.Form):
    # FSH (от 0.1 до 16.4)
    FSH = forms.FloatField(
        label='FSH, mIU/l', min_value=0.1, max_value=16.4, required=True
        )

    # SHBG (от 21.7 до 375.2)
    SHBG = forms.FloatField(
        label='SHBG, nmol/l', min_value=21.7, max_value=375.2, required=True
        )

    # endometr_thick (от 3 до 14)
    endometr_thick = forms.IntegerField(
        label='Endometrial thickness, mm', min_value=3, max_value=14, required=True
        )

    # CRP (от 0.1 до 13.1)
    CRP = forms.FloatField(
        label='CRP, IU/L', min_value=0.1, max_value=13.1, required=True
        )

    # LEP_ADIPOQ (от 0.04 до 15.07)
    LEP_ADIPOQ = forms.FloatField(
        label='Leptin/adiponectin', min_value=0.04, max_value=15.07, required=True
        )
