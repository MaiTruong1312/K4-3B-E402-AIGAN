from pathlib import Path

app_path = Path("codebase/app.py")
content = app_path.read_text(encoding="utf-8")

unified_code = '''PAGE_PARTS = (
    "layout/start.html",
    "components/auth-gate.html",
    "components/instructor-panel.html",
    "screens/01-dashboard.html",
    "screens/02-quiz.html",
    "screens/03-feedback.html",
    "screens/04-retry.html",
    "screens/05-summary.html",
    "views/flowchart.html",
    "layout/end.html",
)
PAGE_PARTS_STUDENT = PAGE_PARTS
PAGE_PARTS_TEACHER = PAGE_PARTS'''

# Replace PAGE_PARTS definitions
import re
content = re.sub(r'PAGE_PARTS_STUDENT = \(.*?\)\n\nPAGE_PARTS_TEACHER = \(.*?\)\nPAGE_PARTS = PAGE_PARTS_STUDENT', unified_code, content, flags=re.DOTALL)

app_path.write_text(content, encoding="utf-8")
print("Unified PAGE_PARTS in codebase/app.py!")
