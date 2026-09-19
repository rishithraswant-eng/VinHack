import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from app.evidence.sealer import SealedEvidence

class DossierGenerator:
    def __init__(self, output_dir: str = "storage/dossiers"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()

    def _draw_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Oblique", 8)
        canvas.setFillColor(colors.gray)
        # Required by specs
        limitations = (
            "LIMITATIONS: This algorithmic attribution is probabilistic. It does not constitute direct evidence of intent. "
            "Model performance may vary. Produced under Section 63 BSA / 65B IEA guidelines."
        )
        # Ensure it's on every page
        canvas.drawString(30, 30, limitations)
        canvas.restoreState()

    def generate_dossier(self, case_ref: str, fir_num: str, io_desig: str, evidence: SealedEvidence) -> str:
        filename = os.path.join(self.output_dir, f"dossier_{evidence.snapshot_id}.pdf")
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=60)
        
        elements = []
        
        # Header
        elements.append(Paragraph(f"FORENSIC TRACE DOSSIER (Section 63 BSA / 65B IEA)", self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Metadata
        elements.append(Paragraph(f"<b>Case Reference:</b> {case_ref}", self.styles['Normal']))
        elements.append(Paragraph(f"<b>FIR Number:</b> {fir_num}", self.styles['Normal']))
        elements.append(Paragraph(f"<b>IO Designation:</b> {io_desig}", self.styles['Normal']))
        elements.append(Paragraph(f"<b>Sealed At:</b> {evidence.sealed_at}", self.styles['Normal']))
        elements.append(Paragraph(f"<b>Snapshot ID:</b> {evidence.snapshot_id}", self.styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Trace Path
        elements.append(Paragraph("<b>Attributed Trace Path [Citation: Graph Engine]</b>", self.styles['Heading2']))
        path = evidence.trace_result.path
        if path:
            elements.append(Paragraph(f"Seed Address: {path[0]}", self.styles['Normal']))
            elements.append(Paragraph(f"Attributed VASP: {evidence.trace_result.vasp_node}", self.styles['Normal']))
            
            data = [["Hop", "Address"]]
            for idx, addr in enumerate(path):
                data.append([str(idx), addr])
                
            t = Table(data, style=[
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            elements.append(t)
        else:
            elements.append(Paragraph("No trace path found.", self.styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Analytics
        elements.append(Paragraph("<b>Analytics & Confidence [Citation: Monte Carlo / Classifier]</b>", self.styles['Heading2']))
        elements.append(Paragraph(f"Classifier Version: {evidence.trace_result.classifier_version}", self.styles['Normal']))
        conf = evidence.trace_result.confidence_result
        elements.append(Paragraph(f"Confidence Score: {conf.score:.4f}", self.styles['Normal']))
        elements.append(Paragraph(f"Confidence Interval: [{conf.ci_low:.4f}, {conf.ci_high:.4f}]", self.styles['Normal']))
        elements.append(Paragraph(f"Requires Review: {conf.requires_review}", self.styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Merkle Proofs
        elements.append(Paragraph("<b>Cryptographic Verification [Citation: Merkle Inclusion]</b>", self.styles['Heading2']))
        for p in evidence.merkle_proofs:
            elements.append(Paragraph(f"Tx Hash: {p.tx_hash}", self.styles['Normal']))
            elements.append(Paragraph(f"Merkle Root: {p.merkle_root}", self.styles['Normal']))
            elements.append(Spacer(1, 6))
            
        # Build Document
        doc.build(elements, onFirstPage=self._draw_footer, onLaterPages=self._draw_footer)
        
        return filename

# Expose at module level for smoke testing
def generate_dossier(case_ref: str, fir_num: str, io_desig: str, evidence: SealedEvidence) -> str:
    gen = DossierGenerator()
    return gen.generate_dossier(case_ref, fir_num, io_desig, evidence)
