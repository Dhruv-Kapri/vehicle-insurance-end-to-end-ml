from typing import Optional

from fastapi import Request


def _to_int(value):
    return int(value) if value is not None else None


def _to_float(value):
    return float(value) if value is not None else None


class DataForm:
    def __init__(self, request: Request):
        self.request = request

        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    async def load_data(self):
        form = await self.request.form()

        self.Gender = _to_int(form.get("Gender"))
        self.Age = _to_int(form.get("Age"))
        self.Driving_License = _to_int(form.get("Driving_License"))
        self.Region_Code = _to_float(form.get("Region_Code"))
        self.Previously_Insured = _to_int(form.get("Previously_Insured"))
        self.Annual_Premium = _to_float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = _to_float(form.get("Policy_Sales_Channel"))
        self.Vintage = _to_int(form.get("Vintage"))
        self.Vehicle_Age_lt_1_Year = _to_int(form.get("Vehicle_Age_lt_1_Year"))
        self.Vehicle_Age_gt_2_Years = _to_int(form.get("Vehicle_Age_gt_2_Years"))
        self.Vehicle_Damage_Yes = _to_int(form.get("Vehicle_Damage_Yes"))
        self.Vehicle_Damage_Yes = _to_int(form.get("Vehicle_Damage_Yes"))
