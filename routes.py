from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import CommandLog, User
import subprocess
import logging
from datetime import datetime
import platform

main = Blueprint('main', __name__)

# Allowed commands whitelist
ALLOWED_COMMANDS = {
    'list_files': 'dir',
    'system_info': 'systeminfo',
    'disk_usage': 'wmic logicaldisk get size,freespace,caption',
    'process_list': 'tasklist',
    'network_info': 'ipconfig'
}

@main.route('/')
def index():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/execute_command', methods=['POST'])
@login_required
def execute_command():
    command_type = request.form.get('command_type')
    
    if command_type not in ALLOWED_COMMANDS:
        return jsonify({'error': 'Invalid command type'}), 400
    
    try:
        # Execute the command with proper Windows command handling
        command = ALLOWED_COMMANDS[command_type]
        logging.info(f"Executing command: {command}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,  # Increased timeout
            shell=True,
            encoding='utf-8',
            errors='replace'  # Handle encoding errors gracefully
        )
        
        # Log the command execution
        log = CommandLog(
            user_id=current_user.id,
            command=command,
            output=result.stdout,
            status='success' if result.returncode == 0 else 'failed'
        )
        db.session.add(log)
        db.session.commit()
        
        # Format the output for better readability
        formatted_output = result.stdout.replace('\r\n', '\n')
        
        return jsonify({
            'output': formatted_output,
            'error': result.stderr,
            'status': 'success' if result.returncode == 0 else 'failed'
        })
        
    except subprocess.TimeoutExpired:
        logging.error(f"Command timed out: {command_type}")
        return jsonify({'error': 'Command timed out'}), 408
    except Exception as e:
        logging.error(f"Error executing command {command_type}: {str(e)}")
        return jsonify({'error': f'Error executing command: {str(e)}'}), 500

@main.route('/command_history')
@login_required
def command_history():
    # Get all command logs with user information
    logs = CommandLog.query.join(User).add_columns(
        CommandLog.id,
        CommandLog.command,
        CommandLog.output,
        CommandLog.timestamp,
        CommandLog.status,
        User.username
    ).order_by(CommandLog.timestamp.desc()).all()
    
    return render_template('history.html', logs=logs) 