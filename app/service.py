from typing import Dict
import tkinter as tk
import csv
from tkinter import filedialog
from .models import Calculation
from fastapi import HTTPException
from .repository import CalculationRepository

class Services:

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


    def operator_priority(operator: str) -> int:
        if operator in ("+", "-"):
            return 1
        if operator in ("*", "/"):
            return 2
        return 0

    async def calculate_infix_operation(self, expression: str) -> Dict[str, str]:
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
                        self.apply_operators(operators, values)
                    operators.pop()
                else:
                    while (operators and self.operator_priority(operators[-1]) >= self.operator_priority(expression[i])):
                        self.apply_operators(operators, values)
                    operators.append(expression[i])
                i += 1

            while operators:
                self.apply_operators(operators, values)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid operation: {e}")
        
        result = str(values[-1])
        calculation = Calculation(operation=expression, result=result)
        await CalculationRepository.insert_calculation(calculation)

        return {"operation": expression, "result": result}
    
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
    
    def get_csv_data_from_db():
        try:
            db_data = CalculationRepository.get_all_db_data()

            root = tk.Tk()
            root.withdraw()
    
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", ".csv"), ("All files", "*.*")],
                title="Save as..."
            )

            if file_path:
                with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["id", "operation", "result", "created_at"])

                    for calculation in db_data:
                        writer.writerow([calculation.id, calculation.operation, calculation.result, calculation.created_at])
            return "Data exported in CSV successfully !"
        except Exception as e:
            raise Exception(f"Failed to export CSV data: {str(e)}")
