from datetime import datetime, timezone
from typing import Dict
import tkinter as tk
import csv
import pytz
import os
from tkinter import filedialog
from .models import Calculation
from fastapi import HTTPException
from .repository import CalculationRepository

EXPORT_DIR = "/app/exports"


class Services:

    @staticmethod
    def apply_operators(operators, values):
        operator = operators.pop()
        value_2 = values.pop()
        value_1 = values.pop()
        if operator == "+":
            values.append(value_1 + value_2)
        elif operator == "-":
            values.append(value_1 - value_2)
        elif operator == "*":
            values.append(value_1 * value_2)
        elif operator == "/":
            values.append(value_1 / value_2)

    @staticmethod
    def operator_priority(operator: str) -> int:
        if operator in ("+", "-"):
            return 1
        if operator in ("*", "/"):
            return 2
        return 0

    @staticmethod
    async def calculate_infix_operation(expression: str) -> Dict[str, str]:
        try:
            operators = []
            values = []
            i = 0

            while i < len(expression):
                if expression[i] == " ":
                    i += 1
                    continue
                elif expression[i] == "(":
                    operators.append("(")
                elif expression[i].isdigit():
                    value = 0
                    while i < len(expression) and expression[i].isdigit():
                        value = (value * 10) + int(expression[i])
                        i += 1
                    values.append(value)
                    i -= 1
                elif expression[i] == ")":
                    while operators and operators[-1] != "(":
                        Services.apply_operators(operators, values)
                    operators.pop()
                else:
                    while (operators and Services.operator_priority(operators[-1]) >= Services.operator_priority(expression[i])):
                        Services.apply_operators(operators, values)
                    operators.append(expression[i])
                i += 1

            while operators:
                Services.apply_operators(operators, values)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid operation: {e}")
        
        result = str(values[-1])
        calculation = Calculation(operation=expression, result=result)
        await CalculationRepository.insert_calculation(calculation)

        return {"operation": expression, "result": result}
    
    @staticmethod
    async def calculate_postfix_operation(expression: str) -> float:
        try:
            pile = []
            for element in expression:
                if element == " ":
                    continue
                if element.isdigit():
                    pile.append(int(element))
                else:
                    value_2 = pile.pop()
                    value_1 = pile.pop()

                if element == "+":
                    result = value_1 + value_2
                    pile.append(result)
                elif element == "-":
                    result = value_1 - value_2
                    pile.append(result)
                elif element == "*":
                    result = value_1 * value_2
                    pile.append(result)
                elif element == "/":
                    result = value_1 / value_2
                    pile.append(result)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid operation: {e}")
        
        result = str(pile.pop())
        calculation = Calculation(operation=expression, result=result)
        await CalculationRepository.insert_calculation(calculation)

        return {"operation": expression, "result": result}
    
    @staticmethod
    async def get_csv_data_from_db():
        try:
            if not os.path.exists(EXPORT_DIR):
                os.makedirs(EXPORT_DIR)

            file_path = os.path.join(EXPORT_DIR, "exported_data.csv")

            db_data = await CalculationRepository.get_all_db_data()
            local_tz = pytz.timezone('Europe/Paris')

            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "operation", "result", "created_at"])

                for calculation in db_data:
                    date_created_utc = datetime.fromtimestamp(calculation.created_at, tz=timezone.utc)
                    date_created_local = date_created_utc.astimezone(local_tz)
                    date_created_str = date_created_local.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([calculation.id, calculation.operation, calculation.result, date_created_str])

            return file_path 
        except Exception as e:
            raise Exception(f"Failed to export CSV data: {str(e)}")
        # -----------------------------------------------
        # FOR TESTING LOCAL WITHOUT DOCKER ENVIRONMENT
        # try:
        #     db_data = await CalculationRepository.get_all_db_data()

        #     root = tk.Tk()
        #     root.withdraw()
    
        #     file_path = filedialog.asksaveasfilename(
        #         defaultextension=".csv",
        #         filetypes=[("CSV files", ".csv"), ("All files", "*.*")],
        #         title="Save as..."
        #     )

        #     if file_path:
        #         with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        #             writer = csv.writer(file)
        #             writer.writerow(["id", "operation", "result", "created_at"])

        #             for calculation in db_data:
        #                 writer.writerow([calculation.id, calculation.operation, calculation.result, calculation.created_at])
        #         return "Data exported in CSV successfully !"
        #     return "No file path provided for CSV export."
        # except Exception as e:
        #     raise Exception(f"Failed to export CSV data: {str(e)}")
        # -----------------------------------------------
