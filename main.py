import os
import time
import json
import hashlib
from datetime import datetime

class SystemLogger:
    def __init__(self, log_file="system_calls.log"):
        self.log_file = log_file
        
    def log(self, username, system_call, status, details=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "username": username,
            "system_call": system_call,
            "status": status,
            "details": details
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self._load_users()
        
    def _load_users(self):
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "admin": {
                    "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                    "role": "admin",
                    "failed_attempts": 0,
                    "locked_until": None
                }
            }
    
    def _save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)
    
    def authenticate(self, username, password):
        if username not in self.users:
            return False
            
        user = self.users[username]
        
        if user.get("locked_until") and time.time() < user["locked_until"]:
            remaining = int(user["locked_until"] - time.time())
            print(f"Account locked. Try again in {remaining} seconds.")
            return False
            
        if user["password_hash"] == hashlib.sha256(password.encode()).hexdigest():
            user["failed_attempts"] = 0
            self._save_users()
            return True
        else:
            user["failed_attempts"] += 1
            if user["failed_attempts"] >= 3:
                user["locked_until"] = time.time() + 300
            self._save_users()
            return False
    
    def create_user(self, username, password, role="user"):
        if username in self.users:
            return False
            
        self.users[username] = {
            "password_hash": hashlib.sha256(password.encode()).hexdigest(),
            "role": role,
            "failed_attempts": 0,
            "locked_until": None
        }
        self._save_users()
        return True

class SystemCallSimulator:
    def __init__(self):
        self.logger = SystemLogger()
        self.user_manager = UserManager()
        self.current_user = None
        
        self.system_calls = {
            "read": {
                "description": "Read from a file",
                "admin_only": False,
                "simulate": self._simulate_read
            },
            "write": {
                "description": "Write to a file",
                "admin_only": False,
                "simulate": self._simulate_write
            },
            "execute": {
                "description": "Execute a program",
                "admin_only": True,
                "simulate": self._simulate_execute
            },
            "delete": {
                "description": "Delete a file",
                "admin_only": True,
                "simulate": self._simulate_delete
            },
            "list": {
                "description": "List directory contents",
                "admin_only": False,
                "simulate": self._simulate_list
            }
        }
    
    def _simulate_read(self, filename):
        return f"Simulated read from {filename}: Sample content"
    
    def _simulate_write(self, filename, content):
        return f"Simulated write to {filename}: {content}"
    
    def _simulate_execute(self, program):
        return f"Simulated execution of {program}"
    
    def _simulate_delete(self, filename):
        return f"Simulated deletion of {filename}"
    
    def _simulate_list(self, directory):
        return f"Simulated directory listing of {directory}: file1.txt, file2.txt, dir1/"
    
    def login(self):
        print("\n=== Login ===")
        username = input("Username: ")
        password = input("Password: ")  # Using input instead of getpass for simplicity
        
        if self.user_manager.authenticate(username, password):
            self.current_user = username
            self.logger.log(username, "login", "success")
            return True
        else:
            self.logger.log(username, "login", "failed")
            return False
    
    def signup(self):
        print("\n=== Signup ===")
        username = input("Username: ")
        password = input("Password: ")
        
        if self.user_manager.create_user(username, password):
            print("User created successfully!")
            self.logger.log(username, "signup", "success")
        else:
            print("Username already exists!")
            self.logger.log(username, "signup", "failed")
    
    def get_allowed_calls(self):
        is_admin = self.user_manager.users[self.current_user]["role"] == "admin"
        return [
            call for call, info in self.system_calls.items()
            if not info["admin_only"] or is_admin
        ]
    
    def execute_call(self, call_name, *args):
        if call_name not in self.system_calls:
            self.logger.log(self.current_user, call_name, "failed", "Invalid system call")
            return "Invalid system call"
            
        call_info = self.system_calls[call_name]
        
        if call_info["admin_only"] and self.user_manager.users[self.current_user]["role"] != "admin":
            self.logger.log(self.current_user, call_name, "failed", "Unauthorized access")
            return "Unauthorized access"
        
        try:
            result = call_info["simulate"](*args)
            self.logger.log(self.current_user, call_name, "success", str(args))
            return result
        except Exception as e:
            self.logger.log(self.current_user, call_name, "failed", str(e))
            return f"Error: {str(e)}"
    
    def show_menu(self):
        while True:
            print("\n=== Secure System Call Interface ===")
            print("1. Login")
            print("2. Signup")
            print("3. Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                if self.login():
                    self.show_system_calls()
            elif choice == "2":
                self.signup()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")
    
    def show_system_calls(self):
        while True:
            print("\n=== Available System Calls ===")
            allowed_calls = self.get_allowed_calls()
            
            for i, call in enumerate(allowed_calls, 1):
                print(f"{i}. {call} - {self.system_calls[call]['description']}")
            
            print(f"{len(allowed_calls) + 1}. Logout")
            
            choice = input("\nEnter your choice: ")
            
            try:
                choice_num = int(choice)
                if choice_num == len(allowed_calls) + 1:
                    self.logger.log(self.current_user, "logout", "success")
                    break
                elif 1 <= choice_num <= len(allowed_calls):
                    call_name = allowed_calls[choice_num - 1]
                    self.handle_system_call(call_name)
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
    
    def handle_system_call(self, call_name):
        print(f"\n=== {call_name.upper()} ===")
        
        if call_name == "read":
            filename = input("Enter filename: ")
            result = self.execute_call(call_name, filename)
        elif call_name == "write":
            filename = input("Enter filename: ")
            content = input("Enter content: ")
            result = self.execute_call(call_name, filename, content)
        elif call_name == "execute":
            program = input("Enter program name: ")
            result = self.execute_call(call_name, program)
        elif call_name == "delete":
            filename = input("Enter filename: ")
            result = self.execute_call(call_name, filename)
        elif call_name == "list":
            directory = input("Enter directory (press Enter for current): ") or "."
            result = self.execute_call(call_name, directory)
        
        print("\nResult:", result)
        input("\nPress Enter to continue...")

def main():
    simulator = SystemCallSimulator()
    simulator.show_menu()

if __name__ == "__main__":
    main()