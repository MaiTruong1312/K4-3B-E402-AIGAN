from pathlib import Path

app_path = Path("codebase/app.py")
content = app_path.read_text(encoding="utf-8")

old_parts = '''PAGE_PARTS = (
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
)'''

new_parts = '''PAGE_PARTS_STUDENT = (
    "layout/start.html",
    "components/auth-gate.html",
    "screens/01-dashboard.html",
    "screens/02-quiz.html",
    "screens/03-feedback.html",
    "screens/04-retry.html",
    "screens/05-summary.html",
    "views/flowchart.html",
    "layout/end.html",
)

PAGE_PARTS_TEACHER = (
    "layout/start.html",
    "components/auth-gate.html",
    "components/instructor-panel.html",
    "views/flowchart.html",
    "layout/end.html",
)
PAGE_PARTS = PAGE_PARTS_STUDENT'''

old_index = '''@app.get("/")
def index() -> HTMLResponse:
    html = "\\n".join((TEMPLATE_ROOT / part).read_text(encoding="utf-8") for part in PAGE_PARTS)
    return HTMLResponse(html)'''

new_index = '''@app.get("/")
@app.get("/student")
def index() -> HTMLResponse:
    html = "\\n".join((TEMPLATE_ROOT / part).read_text(encoding="utf-8") for part in PAGE_PARTS_STUDENT)
    return HTMLResponse(html)


@app.get("/instructor")
@app.get("/teacher")
def instructor_dashboard() -> HTMLResponse:
    html = "\\n".join((TEMPLATE_ROOT / part).read_text(encoding="utf-8") for part in PAGE_PARTS_TEACHER)
    return HTMLResponse(html)'''

content = content.replace(old_parts, new_parts)
content = content.replace(old_index, new_index)

app_path.write_text(content, encoding="utf-8")
print("Successfully patched codebase/app.py!")
