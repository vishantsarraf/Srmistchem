from flask import Blueprint, render_template, request, send_file
from calculations.pdf_utils import add_pdf_header, get_standard_styles, get_standard_table_style, create_graph
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib import colors
import io
import datetime

exp1_bp = Blueprint('exp1', __name__)

@exp1_bp.route('/')
def index():
    return render_template('experiments/exp1.html')

@exp1_bp.route('/calculate', methods=['POST'])
def calculate():
    v1 = float(request.form.get('v1', 0))
    v2 = float(request.form.get('v2', 0))
    n1 = float(request.form.get('n1', 0))
    n2 = float(request.form.get('n2', 0))
    m = float(request.form.get('m', 0))

    hardness = (n1 * v1 * 100) / v2
    ca_hardness = (n1 * v1 * 100 * 40) / (v2 * 1000)
    mg_hardness = hardness - ca_hardness

    result = {
        'hardness': hardness,
        'ca_hardness': ca_hardness,
        'mg_hardness': mg_hardness
    }
    return render_template('experiments/exp1.html', result=result)

@exp1_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    name = request.form.get('name')
    reg_no = request.form.get('reg_no')
    date_str = request.form.get('date', datetime.datetime.now().strftime('%d-%m-%Y'))
    v1 = float(request.form.get('v1', 0))
    v2 = float(request.form.get('v2', 0))
    n1 = float(request.form.get('n1', 0))
    n2 = float(request.form.get('n2', 0))
    m = float(request.form.get('m', 0))

    hardness = (n1 * v1 * 100) / v2
    ca_hardness = (n1 * v1 * 100 * 40) / (v2 * 1000)
    mg_hardness = hardness - ca_hardness

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles, title_style, h2_style, normal_style, calc_style, header_style, subheader_style = get_standard_styles()
    add_pdf_header(elements, 'exp1', date_str, name, reg_no, title_style, normal_style, header_style, subheader_style)

    elements.append(Paragraph("Theory", h2_style))
    elements.append(Paragraph("EDTA reacts with Ca²⁺ and Mg²⁺ ions to form stable complexes. EDTA titrates metal ions in a 1:1 ratio.", normal_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Observations", h2_style))
    observation_data = [['S.No', 'Volume of EDTA (mL)', 'Burette Reading (mL)'],
                        ['1', v1, v2]]
    obs_table = Table(observation_data, colWidths=[50, 100, 100])
    obs_table.setStyle(get_standard_table_style())
    elements.append(obs_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Calculations", h2_style))
    elements.append(Paragraph(f"Hardness as CaCO₃ = (N₁ × V₁ × 100) / V₂ = ({n1} × {v1} × 100) / {v2} = {hardness:.2f} ppm", calc_style))
    elements.append(Paragraph(f"Calcium hardness = (N₁ × V₁ × 100 × 40) / (V₂ × 1000) = {ca_hardness:.2f} ppm", calc_style))
    elements.append(Paragraph(f"Magnesium hardness = Total hardness - Calcium hardness = {mg_hardness:.2f} ppm", calc_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Result", h2_style))
    elements.append(Paragraph(f"Total hardness = {hardness:.2f} ppm", normal_style))
    elements.append(Paragraph(f"Calcium hardness = {ca_hardness:.2f} ppm", normal_style))
    elements.append(Paragraph(f"Magnesium hardness = {mg_hardness:.2f} ppm", normal_style))

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, download_name='exp1.pdf', as_attachment=True)