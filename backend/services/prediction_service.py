from src.pipeline import VehicleData, VehicleDataClassifier


class PredictionService:
    @staticmethod
    def predict(form):
        vehicle_data = VehicleData(
            Gender=form.Gender,
            Age=form.Age,
            Driving_License=form.Driving_License,
            Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured,
            Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel,
            Vintage=form.Vintage,
            Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes,
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        predictor = VehicleDataClassifier()
        value = predictor.predict(dataframe=vehicle_df)[0]

        return "Response-Yes" if value == 1 else "Response-No"
