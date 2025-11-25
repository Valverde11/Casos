import json
import os
from datetime import datetime

class CalculatorModel:
    def __init__(self):
        self.current_input = ""
        self.previous_result = None
        self.pending_operator = None
        self.is_new_input = True
        self.memory = Memory()
        self.logger = OperationLogger()
    
    def append_digit(self, digit):
        if self.is_new_input:
            self.current_input = digit
            self.is_new_input = False
        else:
            self.current_input += digit
    
    def append_decimal(self):
        if self.is_new_input:
            self.current_input = "0."
            self.is_new_input = False
        elif "." not in self.current_input:
            self.current_input += "."
    
    def set_operator(self, operator):
        if self.current_input:
            if self.pending_operator and not self.is_new_input:
                self.calculate()
            try:
                self.previous_result = float(self.current_input)
                self.pending_operator = operator
                self.is_new_input = True
            except ValueError:
                self.current_input = "Error"
                self.is_new_input = True
        elif self.previous_result is not None:
            self.pending_operator = operator
    
    def calculate(self):
        if (self.pending_operator and self.previous_result is not None 
            and self.current_input and not self.is_new_input):
            try:
                current_value = float(self.current_input)
                result = 0
                
                if self.pending_operator == "+":
                    result = self.previous_result + current_value
                elif self.pending_operator == "-":
                    result = self.previous_result - current_value
                elif self.pending_operator == "*":
                    result = self.previous_result * current_value
                elif self.pending_operator == "/":
                    if current_value != 0:
                        result = self.previous_result / current_value
                    else:
                        self.current_input = "Error"
                        self.is_new_input = True
                        return
                
                operation = f"{self.previous_result} {self.pending_operator} {current_value} = {result}"
                self.logger.log_operation(operation)
                
                self.current_input = str(result)
                self.previous_result = result
                self.pending_operator = None
                self.is_new_input = True
            except ValueError:
                self.current_input = "Error"
                self.is_new_input = True
    
    def calculate_equals(self):
        if (self.pending_operator and self.previous_result is not None 
            and self.current_input):
            self.calculate()
        elif not self.current_input and self.previous_result is not None:
            self.current_input = str(self.previous_result)
            self.is_new_input = True
    
    def clear(self):
        if not self.current_input and self.previous_result is not None:
            operation = "C (clear)"
            self.logger.log_operation(operation)
            self.previous_result = None
            self.pending_operator = None
        else:
            self.current_input = ""
        self.is_new_input = True
    
    def add_to_memory(self):
        if self.current_input:
            try:
                value = float(self.current_input)
                self.memory.add_to_memory(value)
                
                memory_contents = self.memory.get_memory_contents()
                operation = f"M+ {value} > {memory_contents}"
                self.logger.log_operation(operation)
            except ValueError:
                pass
    
    def calculate_average(self):
        avg = self.memory.calculate_average()
        self.current_input = str(avg)
        self.is_new_input = True
        
        memory_contents = self.memory.get_memory_contents()
        operation = f"Avg {memory_contents} = {avg}"
        self.logger.log_operation(operation)
    
    def convert_to_binary(self):
        if self.current_input:
            try:
                value = int(float(self.current_input))
                binary = bin(value)[2:]
                self.current_input = binary
                self.is_new_input = True
                
                operation = f"Binario {value} = {binary}"
                self.logger.log_operation(operation)
            except (ValueError, OverflowError):
                self.current_input = "Error"
                self.is_new_input = True
    
    def check_prime(self):
        if self.current_input:
            try:
                value = int(float(self.current_input))
                is_prime = self.is_prime_number(value)
                self.current_input = str(is_prime)
                self.is_new_input = True
                
                operation = f"Primo {value} {is_prime}"
                self.logger.log_operation(operation)
            except (ValueError, OverflowError):
                self.current_input = "Error"
                self.is_new_input = True
    
    def is_prime_number(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def get_current_input(self):
        return self.current_input if self.current_input else "0"
    
    def get_operation_history(self):
        return self.logger.get_operation_history()


class Memory:
    def __init__(self):
        self.memory_size = 10
        self.memory = []
    
    def add_to_memory(self, value):
        if len(self.memory) >= self.memory_size:
            self.memory.pop(0)
        self.memory.append(value)
    
    def calculate_average(self):
        if not self.memory:
            return 0
        return sum(self.memory) / len(self.memory)
    
    def get_memory_contents(self):
        return " ".join(str(x) for x in self.memory)
    
    def get_memory_size(self):
        return len(self.memory)


class OperationLogger:
    def __init__(self):
        self.log_file = "Bitacora.txt"
    
    def log_operation(self, operation):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {operation}"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except IOError as e:
            print(f"Error writing to log file: {e}")
    
    def get_operation_history(self):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                return "No hay operaciones registradas."
        except IOError as e:
            return f"Error reading log file: {e}"