from flask import Flask, render_template, request, jsonify
import logging
import socket

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

# Dictionary with conversion factors to meters (base unit)
CONVERSION_FACTORS = {
    'meters': 1,
    'kilometers': 1000,
    'miles': 1609.34,
    'feet': 0.3048
}

@app.route('/', methods=['GET'])
def index():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return render_template('index.html', hostname=hostname, ip_address=ip_address)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        value = float(data['value'])
        from_unit = data['from_unit'].lower()
        to_unit = data['to_unit'].lower()

        # Convert to meters first (base unit)
        meters = value * CONVERSION_FACTORS[from_unit]
        # Then convert to target unit
        result = meters / CONVERSION_FACTORS[to_unit]

        return jsonify({
            'success': True,
            'result': round(result, 6)
        })
    except (ValueError, KeyError) as e:
        return jsonify({
            'success': False,
            'error': 'Invalid input'
        })

if __name__ == '__main__':
    app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
