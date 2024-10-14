from .models import Calculation
from .db import calculations_collection

class CalculationRepository:

    @staticmethod
    async def insert_calculation(calculation_data: Calculation):
        calculation_dict = calculation_data.model_dump(by_alias=True)
        await calculations_collection.insert_one(calculation_dict)
        print("Calculation inserted")

    # @staticmethod
    # async def get_calculations(limit: int = 100):
    #     calculations = await calculations_collection.find().to_list(limit)
    #     return [Calculation(**calc) for calc in calculations]