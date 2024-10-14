from pydantic import ValidationError
from .models import Calculation
from .db import calculations_collection

class CalculationRepository:

    @staticmethod
    async def insert_calculation(calculation_data: Calculation):
        calculation_dict = calculation_data.model_dump(by_alias=True, exclude_none=True)
        await calculations_collection.insert_one(calculation_dict)
        print("Calculation inserted")
    
    @staticmethod
    async def get_all_db_data() -> list:
        calculations = await calculations_collection.find().to_list()
        results = []
        for calc in calculations:
            try:
                calculation = Calculation(**{**calc, "_id": str(calc["_id"])})
                results.append(calculation)
            except ValidationError as e:
                print(f"Validation failed for document {calc['_id']}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred for document {calc['_id']}: {e}")
        print("Final results:", results)
        return results