# Secure System Calls Web Interface

A secure and intuitive web interface for executing system calls with proper authentication and logging.

## Features

- 🔐 Secure user authentication
- 🖥️ Web-based interface for system calls
- 📝 Comprehensive activity logging
- 🛡️ Input validation and command restriction
- 📊 Real-time command execution feedback

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py
│   └── config.py
├── templates/
│   ├── base.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   ├── css/
│   └── js/
├── logs/
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

## Security Features

- User authentication with password hashing
- Session-based access control
- Command whitelisting
- Comprehensive activity logging
- Input sanitization
- Rate limiting

## Usage

1. Access the web interface at `http://loca5000lhost:`
2. Log in with your credentials
3. Use the dashboard to execute allowed system commands
4. View command history and logs

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details. 