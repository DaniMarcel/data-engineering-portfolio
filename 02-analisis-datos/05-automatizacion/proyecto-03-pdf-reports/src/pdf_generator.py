"""PDF Report Generation"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import pandas as pd
from pathlib import Path
from datetime import datetime

def generate_pdf_report(df, output_path='report.pdf'):
    """Generate PDF report from DataFrame"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>Data Report - {datetime.now().strftime('%Y-%m-%d')}</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Summary
    summary_text = f"""
    <b>Summary:</b><br/>
    Total Records: {len(df):,}<br/>
    Total Revenue: €{df['total'].sum():,.2f}<br/>
    Average Ticket: €{df['total'].mean():.2f}
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Table with top 20
    top_data = df.nlargest(20, 'total')[['producto_nombre', 'total']].values.tolist()
    top_data.insert(0, ['Product', 'Revenue'])
    
    table = Table(top_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    doc.build(story)
    print(f"✅ PDF generated: {output_path}")

if __name__ == "__main__":
    # Buscar carpeta base \'data engineer\'

    current_path = Path(__file__).resolve()

    base_path = None

    for parent in current_path.parents:

        if parent.name == \'data engineer\':

            base_path = parent

            break

    if base_path is None:

        raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")
    df = pd.read_csv(base_path / '02-analisis-datos/01-eda-exploratorio/proyecto-01-ventas-retail/data/raw/transacciones.csv')
    generate_pdf_report(df, 'ventas_report.pdf')
