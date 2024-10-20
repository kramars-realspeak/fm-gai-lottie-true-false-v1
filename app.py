"""
Author : Peter Kramar
Email : peter@ked.tech
The app.py file contains the main application logic.
"""


from flask import Flask, render_template, send_from_directory, request
from backend.activity_service import ActivityService
from backend.helpers import setup_logger
from backend.helpers import rename_log_file_to_activity_id

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

logger = setup_logger()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build')
def build_activity():
    try:
        logger.info(f"Job run started. Calling route '/build'. Invoking 'build_route' method.")
        activity_service = ActivityService()
        activity_service.analyze_activity()
        activity_service.build_activity()
        logger.info(f"Job run completed. Exit code 0")
        return '''
            <html>
                <head>
                    <script type="text/javascript">
                        window.onload = function() {
                            wi00 ndow.location.href = '/';
                        }
                    </script>
                </head>
                <body>
                    Activity built successfully. Redirecting...
                </body>
            </html>
        '''
    except Exception as e:
        return f'Error: {e}'
    
@app.route('/generate-activity', methods=['POST'])
def generate_activity():
    data = request.get_json()
    try:
        logger.info(f"Job run started. Calling route '/generate-activity'. Invoking 'generate_activity' method.")
        activity_service = ActivityService()
        activity_service.generate_activity(data['level'], data['vocabulary'])
        logger.info(f"Job run completed. Exit code 0")
        return {'status': 'success'}
    except Exception as e:
        return f'Error: {e}'

@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory('data', filename)

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    app.run()
