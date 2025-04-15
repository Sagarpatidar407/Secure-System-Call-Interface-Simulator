# Secure System Call Interface

A Python-based simulator for a secure system call interface that enhances security by preventing unauthorized access. The interface includes authentication mechanisms and provides detailed logs of system call usage.

## Features

- Secure authentication system with password hashing
- Role-based access control (admin/user)
- Account locking after failed attempts
- Detailed logging of all system calls
- Simulated system call execution
- User-friendly text-based interface

## System Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/secure-system-interface.git
cd secure-system-interface
```

2. Run the application:
```bash
python main.py
```

## Usage

### Default Admin Account
- Username: `admin`
- Password: `admin123`

### Available System Calls

#### For All Users:
- Read: Read from a file
- Write: Write to a file
- List: List directory contents

#### Admin Only:
- Execute: Execute a program
- Delete: Delete a file

### Logging

All system activities are logged in `system_calls.log` with the following information:
- Timestamp
- Username
- System call type
- Status (success/failed)
- Details

## Security Features

1. **Password Security**
   - Passwords are stored as SHA-256 hashes
   - No plaintext password storage

2. **Access Control**
   - Role-based permissions
   - Admin-only commands
   - User-specific command lists

3. **Account Protection**
   - Account locking after 3 failed attempts
   - 5-minute lockout period

4. **Audit Trail**
   - Comprehensive logging
   - Failed attempt tracking
   - Command execution logging

## Example Usage

1. Start the application:
```bash
python main.py
```

2. Login with admin credentials:
```
Username: admin
Password: admin123
```

3. Create a new user:
```
1. Login
2. Signup
3. Exit
Enter your choice: 2

Username: newuser
Password: password123
```

4. Execute system calls:
```
1. read - Read from a file
2. write - Write to a file
3. list - List directory contents
4. Logout
Enter your choice: 1

Enter filename: test.txt
```

## Logging Format

Logs are stored in JSON format:
```json
{
    "timestamp": "2023-04-15 12:34:56",
    "username": "admin",
    "system_call": "read",
    "status": "success",
    "details": "('test.txt',)"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
