import os
import sys
from flask import Flask, render_template, send_file, redirect

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)
app.secret_key = "chemistry_lab_secret_key_123"

# Fix template path for Vercel
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
app.template_folder = template_dir
app.static_folder = static_dir

EXPERIMENTS = [
    {"id": 3, "name": "DETERMINATION OF THE AMOUNT OF SODIUM CARBONATE AND SODIUM HYDROXIDE IN A MIXTURE BY TITRATION", "slug": "exp3"},
]

# Import experiment blueprints
from calculations.calculation3 import exp3_bp
# from calculations.calculation2 import exp2_bp
# from calculations.calculation3 import exp3_bp
# from calculations.calculation4 import exp4_bp
# from calculations.calculation5 import exp5_bp
# from calculations.calculation6 import exp6_bp
# from calculations.calculation7 import exp7_bp
# from calculations.calculation8 import exp8_bp

# Register blueprints
app.register_blueprint(exp3_bp, url_prefix="/exp3")
# app.register_blueprint(exp2_bp, url_prefix="/exp2")
# app.register_blueprint(exp3_bp, url_prefix="/exp3")
# app.register_blueprint(exp4_bp, url_prefix="/exp4")
# app.register_blueprint(exp5_bp, url_prefix="/exp5")
# app.register_blueprint(exp6_bp, url_prefix="/exp6")
# app.register_blueprint(exp7_bp, url_prefix="/exp7")
# app.register_blueprint(exp8_bp, url_prefix="/exp8")

@app.route('/')
def index():
    return render_template('index.html', experiments=EXPERIMENTS)

@app.route('/view_pdf')
def view_pdf():
    return redirect("https://drive.google.com/file/d/1oAKSQEotat3-estig18W2_i9f3Xj78yv/view?usp=sharing", code=302)

@app.route('/calculations')
def calculations():
    return render_template('experiments.html', experiments=EXPERIMENTS)

@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

# Vercel handler
def handler(request, response):
    return app(request.environ, response.start_response)
