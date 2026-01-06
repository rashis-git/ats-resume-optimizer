"""
PDF Generator for ATS Resume Optimizer
Converts markdown resume to PDF with professional formatting
"""

import re
import io
from fpdf import FPDF
from fpdf.enums import XPos, YPos


class ResumePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(left=18, top=12, right=18)

        # Use Arial TTF for Unicode support (bullet points, special chars)
        # Try Windows font path first, fall back to Helvetica
        try:
            import os
            arial_path = r"C:\Windows\Fonts\arial.ttf"
            arial_bold_path = r"C:\Windows\Fonts\arialbd.ttf"

            if os.path.exists(arial_path):
                self.add_font('Arial', '', arial_path)
                if os.path.exists(arial_bold_path):
                    self.add_font('Arial', 'B', arial_bold_path)
                self.font_family = 'Arial'
            else:
                self.font_family = 'Helvetica'
        except Exception:
            self.font_family = 'Helvetica'

        self.add_page()

    def add_name(self, name):
        """Add name at top - Bold, 12pt, centered"""
        self.set_font(self.font_family, 'B', 12)
        self.cell(0, 6, name, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def add_contact(self, contact):
        """Add contact line - 10pt, centered with clickable links"""
        self.set_font(self.font_family, '', 10)

        # Split contact by | separator
        parts = [p.strip() for p in contact.split('|')]

        # Calculate total width to center the line
        page_width = self.w - self.l_margin - self.r_margin

        # Build parts with links
        contact_parts = []
        for part in parts:
            # Check for markdown link [text](url)
            link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', part)
            if link_match:
                text = link_match.group(1)
                url = link_match.group(2)
                contact_parts.append({'text': text, 'url': url})
            # Check for email
            elif '@' in part and '.' in part:
                email = part.strip()
                contact_parts.append({'text': email, 'url': f'mailto:{email}'})
            else:
                contact_parts.append({'text': part, 'url': None})

        # Calculate total text width
        total_width = 0
        separator = ' | '
        for i, p in enumerate(contact_parts):
            total_width += self.get_string_width(p['text'])
            if i < len(contact_parts) - 1:
                total_width += self.get_string_width(separator)

        # Start position to center
        start_x = self.l_margin + (page_width - total_width) / 2
        self.set_x(start_x)

        # Render each part
        for i, p in enumerate(contact_parts):
            text = p['text']
            url = p['url']
            text_width = self.get_string_width(text)

            if url:
                self.set_text_color(0, 0, 255)  # Blue for links
                self.cell(text_width, 5, text, link=url)
                self.set_text_color(0, 0, 0)  # Back to black
            else:
                self.cell(text_width, 5, text)

            if i < len(contact_parts) - 1:
                self.cell(self.get_string_width(separator), 5, separator)

        self.ln(5)
        self.ln(2)

    def add_section_heading(self, heading):
        """Add section heading - ALL CAPS, Bold"""
        self.ln(4)
        self.set_font(self.font_family, 'B', 10)
        self.cell(0, 6, heading.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def add_subheading(self, text):
        """Add subheading - Bold (Company | Role | Date format)"""
        self.ln(2)
        self.set_font(self.font_family, 'B', 10)
        text = text.replace('**', '')
        available_width = self.w - self.l_margin - self.r_margin
        self.multi_cell(available_width, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_project_subheading(self, text):
        """Add project subheading - Bold"""
        self.ln(1.5)
        self.set_font(self.font_family, 'B', 10)
        text = text.replace('**', '')
        available_width = self.w - self.l_margin - self.r_margin
        self.multi_cell(available_width, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_paragraph(self, text):
        """Add regular paragraph text"""
        self.set_font(self.font_family, '', 10)
        text = self._clean_markdown(text)
        available_width = self.w - self.l_margin - self.r_margin
        self.multi_cell(available_width, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_bullet(self, text):
        """Add bullet point"""
        self.ln(0.5)
        self.set_font(self.font_family, '', 10)
        text = self._clean_markdown(text)
        bullet_char = "-"  # Use dash for compatibility
        indent = 5
        available_width = self.w - self.l_margin - self.r_margin - indent
        self.set_x(self.l_margin + indent)
        self.multi_cell(available_width, 5, f"{bullet_char} {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_education_item(self, text):
        """Add education bullet"""
        self.ln(0.5)
        self.set_font(self.font_family, '', 10)
        bullet_char = "-"
        indent = 5
        available_width = self.w - self.l_margin - self.r_margin - indent
        self.set_x(self.l_margin + indent)
        text = self._clean_markdown(text)
        self.multi_cell(available_width, 5, f"{bullet_char} {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_indented_text(self, text):
        """Add indented text (for education details)"""
        self.set_font(self.font_family, '', 10)
        text = self._clean_markdown(text)
        indent = 8
        available_width = self.w - self.l_margin - self.r_margin - indent
        self.set_x(self.l_margin + indent)
        self.multi_cell(available_width, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def add_skill_line(self, text):
        """Add skill line"""
        self.ln(0.5)
        self.set_font(self.font_family, '', 10)
        bullet_char = "-"
        indent = 5
        available_width = self.w - self.l_margin - self.r_margin - indent
        self.set_x(self.l_margin + indent)
        text = self._clean_markdown(text)
        self.multi_cell(available_width, 5, f"{bullet_char} {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def _clean_markdown(self, text):
        """Remove markdown formatting markers"""
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        return text


def parse_markdown_resume(md_content):
    """Parse markdown resume into structured sections"""
    lines = md_content.strip().split('\n')

    result = {
        'name': '',
        'contact': '',
        'sections': []
    }

    current_section = None
    current_content = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line and not result['name']:
            i += 1
            continue

        # Handle name - could be # Name or **Name** at the start
        if not result['name']:
            if line.startswith('# '):
                result['name'] = line[2:].strip()
                i += 1
                continue
            elif line.startswith('**') and line.endswith('**') and not line.startswith('## '):
                result['name'] = line.strip('*').strip()
                i += 1
                continue
            elif i == 0 and line and not line.startswith('#') and not line.startswith('-') and '@' not in line:
                # First non-empty line might be the name
                result['name'] = line.strip('*').strip()
                i += 1
                continue

        # Handle contact line (contains @ or | typically)
        if result['name'] and not result['contact'] and line and not line.startswith('#') and not line.startswith('-'):
            if '@' in line or '|' in line or 'linkedin' in line.lower():
                result['contact'] = line
                i += 1
                continue

        if line.startswith('## '):
            if current_section:
                result['sections'].append({
                    'heading': current_section,
                    'content': current_content
                })
            current_section = line[3:].strip()
            current_content = []
            i += 1
            continue

        if line == '---':
            i += 1
            continue

        if current_section and line:
            current_content.append(line)

        i += 1

    if current_section:
        result['sections'].append({
            'heading': current_section,
            'content': current_content
        })

    return result


def create_pdf_bytes(md_content: str) -> bytes:
    """
    Convert markdown resume to PDF and return as bytes

    Args:
        md_content: Resume in markdown format

    Returns:
        PDF file as bytes
    """
    # Strip out "Changes Summary" section if present (LLM adds this at the end)
    # Look for common variations
    for separator in ["## Changes Summary", "## Change Summary", "---\n## Changes",
                      "---\n\n## Changes", "# Changes Summary", "**Changes Summary**"]:
        if separator in md_content:
            md_content = md_content.split(separator)[0].strip()
            break

    # Parse markdown
    data = parse_markdown_resume(md_content)

    # Create PDF
    pdf = ResumePDF()

    # Add name
    if data['name']:
        pdf.add_name(data['name'])

    # Add contact
    if data['contact']:
        pdf.add_contact(data['contact'])

    # Add sections
    for section in data['sections']:
        pdf.add_section_heading(section['heading'])
        section_name = section['heading'].upper()

        for line in section['content']:
            if section_name == 'EXPERIENCE':
                if line.startswith('**') and ('|' in line or '(' in line):
                    pdf.add_subheading(line)
                elif line.startswith('- ') or line.startswith('* '):
                    pdf.add_bullet(line[2:])
                else:
                    pdf.add_paragraph(line)

            elif section_name == 'PROJECTS':
                if line.startswith('**'):
                    pdf.add_project_subheading(line)
                elif line.startswith('- ') or line.startswith('* '):
                    pdf.add_bullet(line[2:])
                else:
                    pdf.add_paragraph(line)

            elif section_name == 'EDUCATION':
                if line.startswith('- **') or line.startswith('* **'):
                    pdf.add_education_item(line[2:])
                elif line.startswith('- ') or line.startswith('* '):
                    pdf.add_education_item(line[2:])
                elif line.startswith('  '):
                    pdf.add_indented_text(line.strip())
                else:
                    pdf.add_paragraph(line)

            elif section_name == 'SKILLS':
                if line.startswith('- ') or line.startswith('* '):
                    pdf.add_skill_line(line[2:])
                else:
                    pdf.add_paragraph(line)

            elif section_name == 'CERTIFICATIONS':
                if line.startswith('- ') or line.startswith('* '):
                    pdf.add_bullet(line[2:])
                else:
                    pdf.add_paragraph(line)

            else:
                if line.startswith('- ') or line.startswith('* '):
                    pdf.add_bullet(line[2:])
                elif line.startswith('**'):
                    pdf.add_subheading(line)
                else:
                    pdf.add_paragraph(line)

    # Return as bytes
    return bytes(pdf.output())
