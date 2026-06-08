import re
from pathlib import Path

# Paths
HTML_PATH = Path(r'D:/antigravity_scratch/real_estate_scoring/sql/Ho So Benh An Dung 1955/patient_profile.html')
SUMMARY_MD = Path(r'D:/antigravity_scratch/real_estate_scoring/sql/Ho So Benh An Dung 1955/patient_summary.md')

# Simple helper to extract text between labels (Vietnamese)
def extract(label, text):
    # Look for 'label' followed by ':' and capture until next newline or HTML tag.
    pattern = re.compile(rf"{re.escape(label)}\s*[:：]\s*([^<\n]*)", re.IGNORECASE)
    m = pattern.search(text)
    return m.group(1).strip() if m else None

if not HTML_PATH.exists():
    raise FileNotFoundError(f"HTML file not found: {HTML_PATH}")

content = HTML_PATH.read_text(encoding='utf-8')

# Attempt to find common fields. Adjust as needed based on actual page structure.
patient_name = extract('Tên bệnh nhân', content) or extract('Họ và tên', content)
patient_id = extract('Mã số bệnh nhân', content)
record_number = extract('Số hồ sơ', content) or extract('Số hồ sơ bệnh nhân', content)
diagnosis = extract('Chẩn đoán', content)
admission_date = extract('Ngày nhập viện', content) or extract('Ngày', content)
summary = f"# Thông tin bệnh nhân Dũng\n\n" \
          f"- **Tên**: {patient_name or 'Không xác định'}\n" \
          f"- **Mã số bệnh nhân**: {patient_id or 'Không xác định'}\n" \
          f"- **Số hồ sơ**: {record_number or 'Không xác định'}\n" \
          f"- **Chẩn đoán**: {diagnosis or 'Không xác định'}\n" \
          f"- **Ngày nhập viện**: {admission_date or 'Không xác định'}\n"

# Write summary markdown
SUMMARY_MD.write_text(summary, encoding='utf-8')
print('Summary written to', SUMMARY_MD)
