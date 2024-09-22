"""
Author : Peter Kramar
Email : peter@ked.tech
The app.py file contains the main application logic.
"""


from flask import Flask, render_template, send_from_directory
from backend.activity_service import ActivityService

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build')
def build_activity():
    activity_service = ActivityService()
    try:
        activity_service.analyze_activity()
        activity_service.build_activity()
        return '''
            <html>
                <head>
                    <script type="text/javascript">
                        window.onload = function() {
                            window.location.href = '/';
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

@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory('data', filename)

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    app.run()
