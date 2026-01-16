from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
import io
import os

app = Flask(__name__)

def calculate_risk_score(age, sex, cp, trestbps, chol, thalach, exang):
    """Calculate cardiovascular risk score based on input parameters"""
    score = 0
    risk_factors = []
    
    # Age factor
    if age > 65:
        score += 3
        risk_factors.append(f"Age over 65 ({age} years)")
    elif age > 50:
        score += 2
        risk_factors.append(f"Age over 50 ({age} years)")
    elif age > 40:
        score += 1
    
    # Cholesterol factor
    if chol > 240:
        score += 3
        risk_factors.append(f"High cholesterol ({chol} mg/dL)")
    elif chol > 200:
        score += 2
        risk_factors.append(f"Borderline high cholesterol ({chol} mg/dL)")
    
    # Blood pressure factor
    if trestbps > 140:
        score += 3
        risk_factors.append(f"High blood pressure ({trestbps} mmHg)")
    elif trestbps > 120:
        score += 1
        risk_factors.append(f"Elevated blood pressure ({trestbps} mmHg)")
    
    # Heart rate factor
    if thalach < 100:
        score += 2
        risk_factors.append(f"Low maximum heart rate ({thalach} bpm)")
    
    # Chest pain type
    if cp >= 2:
        score += 2
        risk_factors.append(f"Significant chest pain (type {cp})")
    
    # Exercise induced angina
    if exang == 1:
        score += 2
        risk_factors.append("Exercise-induced chest pain")
    
    # Sex factor (males generally higher risk)
    if sex == 1:
        score += 1
    
    # Determine risk level
    if score >= 8:
        risk_level = "High Risk"
        risk_color = "red"
        recommendation = "Please consult a cardiologist immediately for comprehensive evaluation."
    elif score >= 5:
        risk_level = "Moderate Risk"
        risk_color = "orange"
        recommendation = "Schedule an appointment with your doctor for cardiovascular assessment."
    else:
        risk_level = "Low Risk"
        risk_color = "green"
        recommendation = "Maintain healthy lifestyle habits and regular check-ups."
    
    return {
        'score': score,
        'level': risk_level,
        'color': risk_color,
        'recommendation': recommendation,
        'factors': risk_factors
    }

def generate_pdf_report(data, risk_result):
    """Generate PDF report for cardiovascular risk assessment"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("Cardiovascular Risk Assessment Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report date
    date_text = f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    story.append(Paragraph(date_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment Result
    story.append(Paragraph("Risk Assessment Result", heading_style))
    
    # Risk level box
    risk_color_map = {
        'red': colors.red,
        'orange': colors.orange,
        'green': colors.green
    }
    
    risk_data = [
        ['Risk Level:', risk_result['level']],
        ['Risk Score:', f"{risk_result['score']}/15"]
    ]
    
    risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (1, 0), (1, 0), risk_color_map.get(risk_result['color'], colors.black)),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    story.append(risk_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Patient Data
    story.append(Paragraph("Patient Information", heading_style))
    
    sex_label = "Male" if data['sex'] == '1' else "Female"
    exang_label = "Yes" if data['exang'] == '1' else "No"
    
    patient_data = [
        ['Parameter', 'Value', 'Reference Range'],
        ['Age', f"{data['age']} years", 'N/A'],
        ['Sex', sex_label, 'N/A'],
        ['Resting Blood Pressure', f"{data['trestbps']} mmHg", 'Normal: <120'],
        ['Cholesterol', f"{data['chol']} mg/dL", 'Normal: <200'],
        ['Max Heart Rate', f"{data['thalach']} bpm", 'Normal: 100-180'],
        ['Chest Pain Type', data['cp'], '0-3 scale'],
        ['Exercise Induced Angina', exang_label, 'N/A']
    ]
    
    patient_table = Table(patient_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Risk Factors
    if risk_result['factors']:
        story.append(Paragraph("Identified Risk Factors", heading_style))
        for factor in risk_result['factors']:
            story.append(Paragraph(f"• {factor}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Recommendation
    story.append(Paragraph("Recommendation", heading_style))
    story.append(Paragraph(risk_result['recommendation'], styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Disclaimer
    story.append(Paragraph("Important Disclaimer", heading_style))
    disclaimer_text = """This assessment is for informational purposes only and should not be considered 
    as medical advice. Please consult with a qualified healthcare professional for proper diagnosis 
    and treatment. This tool uses simplified risk calculation and may not account for all individual 
    health factors."""
    story.append(Paragraph(disclaimer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'cp': int(request.form['cp']),
            'trestbps': int(request.form['trestbps']),
            'chol': int(request.form['chol']),
            'thalach': int(request.form['thalach']),
            'exang': int(request.form['exang'])
        }
        
        risk_result = calculate_risk_score(**data)
        
        # Store data in session-like manner (for PDF generation)
        app.config['LAST_ASSESSMENT'] = {
            'data': {k: str(v) for k, v in data.items()},
            'result': risk_result
        }
        
        return render_template('index.html', 
                             prediction_text=f"{risk_result['level']} - Score: {risk_result['score']}/15",
                             risk_color=risk_result['color'],
                             recommendation=risk_result['recommendation'],
                             risk_factors=risk_result['factors'],
                             show_download=True)
    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

@app.route('/download_report')
def download_report():
    try:
        if 'LAST_ASSESSMENT' not in app.config:
            return "No assessment data available. Please complete an assessment first.", 400
        
        assessment = app.config['LAST_ASSESSMENT']
        pdf_buffer = generate_pdf_report(assessment['data'], assessment['result'])
        
        filename = f"cardiovascular_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return f"Error generating report: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)