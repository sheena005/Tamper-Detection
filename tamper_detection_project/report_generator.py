from reportlab.pdfgen import canvas
import datetime

def generate_report(filename, algorithm, root_hash, result, proof):

    report_name = "evidence_report.pdf"

    c = canvas.Canvas(report_name)

    c.setFont("Helvetica", 12)

    c.drawString(100,800,"Digital Evidence Verification Report")

    c.drawString(100,760,f"File Name: {filename}")
    c.drawString(100,730,f"Hash Algorithm: {algorithm}")
    c.drawString(100,700,f"Merkle Root: {root_hash}")
    c.drawString(100,670,f"Verification Result: {result}")

    timestamp = datetime.datetime.now()

    c.drawString(100,640,f"Timestamp: {timestamp}")

    c.drawString(100,600,"Merkle Proof:")

    y = 570

    for p in proof[:10]:
        c.drawString(120,y,p[:30])
        y -= 20

    c.save()

    return report_name