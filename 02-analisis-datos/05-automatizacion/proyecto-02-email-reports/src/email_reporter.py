"""Automated Email Reports"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from datetime import datetime

def generar_reporte_html(df):
    """Generate HTML report"""
    html = f"""
    <html>
    <head><style>
        table {{border-collapse: collapse; width: 100%;}}
        th, td {{border: 1px solid black; padding: 8px; text-align: left;}}
        th {{background-color: #4CAF50; color: white;}}
    </style></head>
    <body>
        <h2>Reporte Diario - {datetime.now().strftime('%Y-%m-%d')}</h2>
        <h3>Resumen</h3>
        <p>Total registros: {len(df):,}</p>
        <p>Ingresos totales: €{df['total'].sum():,.2f}</p>
        <h3>Top 10 Ventas</h3>
        {df.nlargest(10, 'total')[['fecha', 'producto_nombre', 'total']].to_html(index=False)}
    </body>
    </html>
    """
    return html

def enviar_email(destinatario, asunto, html_content, archivo_adjunto=None):
    """Send email with HTML and attachments"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = 'reports@company.com'
    msg['To'] = destinatario
    
    msg.attach(MIMEText(html_content, 'html'))
    
    if archivo_adjunto:
        with open(archivo_adjunto, 'rb') as f:
            attach = MIMEApplication(f.read(), Name=archivo_adjunto.name)
            attach['Content-Disposition'] = f'attachment; filename="{archivo_adjunto.name}"'
            msg.attach(attach)
    
    print(f"📧 Email generado para: {destinatario}")
    print(f"   Asunto: {asunto}")
    # In production: smtp.send_message(msg)

if __name__ == "__main__":
    from pathlib import Path
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
    
    html = generar_reporte_html(df)
    enviar_email("manager@company.com", "Reporte Diario de Ventas", html)
    print("✅ Reporte generado!")
