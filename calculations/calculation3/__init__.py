from flask import Blueprint, render_template, request, send_file
import io
import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

exp3_bp = Blueprint('exp3', __name__)

def safe_float(val, default=0):
    try:
        return float(val) if val is not None else default
    except (TypeError, ValueError):
        return default

def safe_str(val, default=''):
    return str(val) if val is not None else default

@exp3_bp.route('/')
def index():
    return render_template('exp3/index.html')

@exp3_bp.route('/calculate', methods=['POST'])
def calculate():
    result_data = request.form.get('result_data')
    if result_data:
        return {'status': 'success', 'data': json.loads(result_data)}
    return {'status': 'error'}

@exp3_bp.route('/download_pdf', methods=['POST'])
def download_pdf():
    from calculations.pdf_utils import get_standard_styles, add_pdf_header, get_standard_table_style
    result_data = json.loads(request.form.get('result_data', '{}'))
    table_data = json.loads(request.form.get('table_data', '{}'))
    student_name = request.form.get('student_name', '')
    reg_number = request.form.get('reg_number', '')
    
    for key in result_data:
        if result_data[key] is None:
            result_data[key] = 0
    
    for key in table_data:
        if isinstance(table_data[key], list):
            for row in table_data[key]:
                for row_key in row:
                    if row[row_key] is None:
                        row[row_key] = ''
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    styles, title_style, h2_style, normal_style, calc_style, header_style, subheader_style = get_standard_styles()
    
    elements = []
    
    add_pdf_header(elements, 'exp3', datetime.now().strftime('%d-%m-%Y'), student_name, reg_number, title_style, normal_style, header_style, subheader_style)
    
    # Titration 1
    elements.append(Paragraph("TITRATION 1 - STANDARDIZATION OF NaOH", h2_style))
    if table_data.get('t1'):
        table_list = [['S.N.', 'Initial Reading\n(ml)', 'Final Reading\n(ml)', 'Volume of HCl\nUsed (ml)', 'Concordant\nValue']]
        v_concordant = safe_float(result_data.get('v1', 0))
        for i, row in enumerate(table_data['t1'], 1):
            vol = safe_float(row.get('volume', 0))
            is_concordant = abs(vol - v_concordant) < 0.01 if v_concordant > 0 else False
            vols = [safe_float(r.get('volume', 0)) for r in table_data['t1']]
            min_idx = vols.index(min([v for v in vols if v > 0])) if any(v > 0 for v in vols) else -1
            concordant_val = str(round(v_concordant, 2)) if is_concordant and i - 1 == min_idx else '-'
            table_list.append([str(i), str(row.get('initial', '')), str(row.get('final', '')), str(row.get('volume', '')), concordant_val])
        
        t = Table(table_list, colWidths=[40, 90, 90, 100, 80])
        t.setStyle(get_standard_table_style())
        elements.append(t)
        elements.append(Spacer(1, 15))
    else:
        elements.append(Paragraph("- No titration readings -", normal_style))
        elements.append(Spacer(1, 15))
        
    elements.append(Paragraph("Calculation:", ParagraphStyle('calc', parent=normal_style, fontName='Helvetica-Bold')))
    elements.append(Paragraph(f"Formula: N(HCl) = (N(NaOH) × V(NaOH)) / V(HCl)", normal_style))
    norm_naoh = safe_float(result_data.get('normNaoh', 0))
    vol_naoh = safe_float(result_data.get('volNaoh', 0))
    v1 = safe_float(result_data.get('v1', 0))
    norm_acid = safe_float(result_data.get('normAcid', 0))
    elements.append(Paragraph(f"         = ({norm_naoh:.4f} × {vol_naoh:.2f}) / {v1:.2f}", calc_style))
    elements.append(Paragraph(f"         = {norm_acid:.4f} N", calc_style))
    elements.append(Spacer(1, 15))
    
    # Titration 2
    elements.append(Paragraph("TITRATION 2 - PHENOLPHTHALEIN ENDPOINT (Vp)", h2_style))
    if table_data.get('t2'):
        table_list = [['S.N.', 'Initial Reading\n(ml)', 'Final Reading\n(ml)', 'Volume of HCl\nUsed (ml)', 'Concordant\nValue']]
        v_concordant = safe_float(result_data.get('Vp', 0))
        for i, row in enumerate(table_data['t2'], 1):
            vol = safe_float(row.get('volume', 0))
            is_concordant = abs(vol - v_concordant) < 0.01 if v_concordant > 0 else False
            vols = [safe_float(r.get('volume', 0)) for r in table_data['t2']]
            min_idx = vols.index(min([v for v in vols if v > 0])) if any(v > 0 for v in vols) else -1
            concordant_val = str(round(v_concordant, 2)) if is_concordant and i - 1 == min_idx else '-'
            table_list.append([str(i), str(row.get('initial', '')), str(row.get('final', '')), str(row.get('volume', '')), concordant_val])
        
        t = Table(table_list, colWidths=[40, 90, 90, 100, 80])
        t.setStyle(get_standard_table_style())
        elements.append(t)
        elements.append(Spacer(1, 15))
    else:
        elements.append(Paragraph("- No titration readings -", normal_style))
        elements.append(Spacer(1, 15))
        
    # Titration 3
    elements.append(Paragraph("TITRATION 3 - METHYL ORANGE ENDPOINT (Vm)", h2_style))
    if table_data.get('t3'):
        table_list = [['S.N.', 'Initial Reading\n(ml)', 'Final Reading\n(ml)', 'Volume of HCl\nUsed (ml)', 'Concordant\nValue']]
        v_concordant = safe_float(result_data.get('Vm', 0))
        for i, row in enumerate(table_data['t3'], 1):
            vol = safe_float(row.get('volume', 0))
            is_concordant = abs(vol - v_concordant) < 0.01 if v_concordant > 0 else False
            vols = [safe_float(r.get('volume', 0)) for r in table_data['t3']]
            min_idx = vols.index(min([v for v in vols if v > 0])) if any(v > 0 for v in vols) else -1
            concordant_val = str(round(v_concordant, 2)) if is_concordant and i - 1 == min_idx else '-'
            table_list.append([str(i), str(row.get('initial', '')), str(row.get('final', '')), str(row.get('volume', '')), concordant_val])
        
        t = Table(table_list, colWidths=[40, 90, 90, 100, 80])
        t.setStyle(get_standard_table_style())
        elements.append(t)
        elements.append(Spacer(1, 15))
    else:
        elements.append(Paragraph("- No titration readings -", normal_style))
        elements.append(Spacer(1, 15))
        
    elements.append(Paragraph("CALCULATIONS", h2_style))
    vp = safe_float(result_data.get('Vp', 0))
    vm = safe_float(result_data.get('Vm', 0))
    norm_acid = safe_float(result_data.get('normAcid', 0))
    strength_naoh = safe_float(result_data.get('strengthNaoh', 0))
    amount_naoh = safe_float(result_data.get('amountNaoh', 0))
    amount_nahco3 = safe_float(result_data.get('amountNahco3', 0))
    
    elements.append(Paragraph("Formula: Strength of NaOH = [2×Vp − Vm] × Strength of HCl / 20", normal_style))
    elements.append(Paragraph(f"         = [2×{vp:.2f} − {vm:.2f}] × {norm_acid:.4f} / 20", calc_style))
    elements.append(Paragraph(f"         = {strength_naoh:.4f} g/L", calc_style))
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("Formula: Amount of NaOH = Strength × 40", normal_style))
    elements.append(Paragraph(f"         = {strength_naoh:.4f} × 40", calc_style))
    elements.append(Paragraph(f"         = {amount_naoh:.4f} g/L", calc_style))
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("Formula: Strength of Na2CO3 = [2×(Vm − Vp) × Strength of HCl] / 20", normal_style))
    elements.append(Paragraph(f"         = [2×({vm:.2f} − {vp:.2f}) × {norm_acid:.4f}] / 20", calc_style))
    elements.append(Paragraph(f"         = {amount_nahco3:.4f} g/L", calc_style))
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("FINAL RESULT", h2_style))
    elements.append(Paragraph(f"The Amount of NaOH is {amount_naoh:.4f} g/L", normal_style))
    elements.append(Paragraph(f"The Amount of Na2CO3 is {amount_nahco3:.4f} g/L", normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"Exp3_{reg_number}.pdf", mimetype='application/pdf')

@exp3_bp.route('/reset')
def reset():
    return render_template('exp3/index.html')