function switchAuthRole(role) {
  const isStudent = role === 'student';
  const studentForm = document.getElementById('student-login-form');
  const teacherForm = document.getElementById('teacher-login-form');
  const tabStudent = document.getElementById('auth-tab-student');
  const tabTeacher = document.getElementById('auth-tab-teacher');
  const authError = document.getElementById('auth-error');

  if (studentForm) studentForm.style.display = isStudent ? 'block' : 'none';
  if (teacherForm) teacherForm.style.display = isStudent ? 'none' : 'block';
  if (tabStudent) tabStudent.classList.toggle('active', isStudent);
  if (tabTeacher) tabTeacher.classList.toggle('active', !isStudent);
  if (authError) authError.textContent = '';
}

function closeAuthGate() {
  const authGate = document.getElementById('auth-gate');
  if (authGate) authGate.style.display = 'none';
}

async function postAuth(url, payload) {
  const response = await fetch(url, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || 'Không đăng nhập được');
  return data;
}

function rememberAuth(data) {
  learningSessionId = data.session_id;
  localStorage.setItem('vlearn_session_id', data.session_id);
  localStorage.setItem('vlearn_role', data.role);
  localStorage.setItem('vlearn_display_name', data.display_name);
}

function showTeacherWorkspace(displayName) {
  const authGate = document.getElementById('auth-gate');
  const mainContainer = document.querySelector('main.container');
  const interactiveView = document.getElementById('interactive-view');
  const diagramView = document.getElementById('diagram-view');
  const stepNavBar = document.getElementById('step-nav-bar');
  const instructorPanel = document.getElementById('instructor-panel');
  const avatar = document.getElementById('current-user-avatar');

  if (authGate) authGate.style.display = 'none';
  if (mainContainer) mainContainer.style.display = '';
  if (interactiveView) interactiveView.style.display = 'none';
  if (diagramView) diagramView.style.display = 'none';
  if (stepNavBar) stepNavBar.style.display = 'none';
  if (instructorPanel) instructorPanel.style.display = 'block';

  if (avatar) {
    avatar.textContent = (displayName || 'GV').slice(0, 2).toUpperCase();
    avatar.title = `Giảng viên: ${displayName || 'Giảng viên'}`;
  }
}

function showStudentWorkspace(displayName) {
  const authGate = document.getElementById('auth-gate');
  const mainContainer = document.querySelector('main.container');
  const interactiveView = document.getElementById('interactive-view');
  const diagramView = document.getElementById('diagram-view');
  const stepNavBar = document.getElementById('step-nav-bar');
  const instructorPanel = document.getElementById('instructor-panel');
  const avatar = document.getElementById('current-user-avatar');
  const title = document.getElementById('student-welcome-title');

  if (authGate) authGate.style.display = 'none';
  if (instructorPanel) instructorPanel.style.display = 'none';
  if (diagramView) diagramView.style.display = 'none';
  if (mainContainer) mainContainer.style.display = '';
  if (interactiveView) interactiveView.style.display = 'block';
  if (stepNavBar) stepNavBar.style.display = 'flex';

  if (avatar) {
    avatar.textContent = (displayName || 'HV').slice(0, 2).toUpperCase();
    avatar.title = `Học viên: ${displayName || 'Học viên'}`;
  }
  if (title) title.textContent = `Chào bạn, học viên ${displayName || ''}!`;
  if (typeof goToStep === 'function') {
    goToStep(typeof currentStep === 'number' && currentStep > 0 ? currentStep : 1);
  }
}

async function loginStudent(event) {
  event.preventDefault();
  try {
    const data = await postAuth('/api/auth/student', {
      student_code: document.getElementById('student-code').value.trim()
    });
    rememberAuth(data);
    showStudentWorkspace(data.display_name);
  } catch (error) {
    document.getElementById('auth-error').textContent = error.message;
  }
}

async function loginTeacher(event) {
  event.preventDefault();
  try {
    const data = await postAuth('/api/auth/teacher', {
      username: document.getElementById('teacher-username').value,
      password: document.getElementById('teacher-password').value
    });
    rememberAuth(data);
    showTeacherWorkspace(data.display_name);
    await loadInstructorReport();
  } catch (error) {
    document.getElementById('auth-error').textContent = error.message;
  }
}

async function loadInstructorReport() {
  if (!learningSessionId) throw new Error('Thiếu session_id giảng viên');
  const response = await fetch(`/api/instructor/report?session_id=${encodeURIComponent(learningSessionId)}`);
  const report = await response.json();
  if (!response.ok) throw new Error(report.detail || 'Không tải được báo cáo');
  const root = document.getElementById('instructor-report-content');
  if (!root) return;
  root.replaceChildren();

  function formatDecision(decision) {
    if (!decision) return 'Chưa có lượt nộp';
    if (decision === 'VERIFY') return 'Hiểu bài / Đã xác nhận';
    if (decision === 'DIAGNOSE') return 'Chẩn đoán lỗ hổng kiến thức';
    if (decision === 'CLARIFY') return 'Yêu cầu làm rõ cách nghĩ';
    if (decision === 'DECLINE') return 'Từ chối / Nhập lại';
    return decision;
  }

  const sections = [
    [
      'Danh sách Học viên & Tiến độ làm bài',
      report.student_sessions || [],
      item => `Học viên: ${item.student_code || 'Khách (Chưa đặt mã)'} · ${item.total_attempts} lượt làm bài · Trạng thái phiên: ${item.status === 'complete' ? 'Đã hoàn thành' : 'Đang học'} · Đánh giá gần nhất: ${formatDecision(item.latest_decision)} ${item.latest_assessment_type ? `(${item.latest_assessment_type})` : ''}`
    ],
    [
      'Lỗi phổ biến',
      report.misconceptions || [],
      item => `${item.concept}: ${item.misconception || item.misconception_id} · ${item.occurrences} lượt`
    ],
    [
      'Câu hỏi cần duyệt',
      report.question_flags || [],
      item => `${item.question_id}: ${item.issue} · ${item.status}`
    ],
    [
      'Phân loại phản hồi',
      report.assessment_counts || [],
      item => `${item.assessment_type}: ${item.total}`
    ]
  ];

  sections.forEach(([title, items, format]) => {
    const card = document.createElement('section');
    card.className = 'instructor-report-card';
    const heading = document.createElement('h2'); heading.textContent = title; card.appendChild(heading);
    if (!items.length) { const empty = document.createElement('p'); empty.textContent = 'Chưa có dữ liệu.'; card.appendChild(empty); }
    items.forEach(item => { const row = document.createElement('div'); row.className = 'instructor-report-row'; row.textContent = format(item); card.appendChild(row); });
    root.appendChild(card);
  });
}

function logoutUser() {
  localStorage.removeItem('vlearn_session_id');
  localStorage.removeItem('vlearn_role');
  localStorage.removeItem('vlearn_display_name');
  window.location.reload();
}

function switchAccount() {
  localStorage.removeItem('vlearn_session_id');
  localStorage.removeItem('vlearn_role');
  localStorage.removeItem('vlearn_display_name');
  learningSessionId = null;
  const instructorPanel = document.getElementById('instructor-panel');
  if (instructorPanel) instructorPanel.style.display = 'none';
  const mainContainer = document.querySelector('main.container');
  if (mainContainer) mainContainer.style.display = '';
  const interactiveView = document.getElementById('interactive-view');
  if (interactiveView) interactiveView.style.display = 'none';
  const stepNavBar = document.getElementById('step-nav-bar');
  if (stepNavBar) stepNavBar.style.display = 'none';
  const authGate = document.getElementById('auth-gate');
  if (authGate) authGate.style.display = 'grid';

  const isInstructorPage = window.location.pathname.includes('/instructor') || window.location.pathname.includes('/teacher');
  switchAuthRole(isInstructorPage ? 'teacher' : 'student');
}

function closeLessonOverview() {
  const panel = document.getElementById('lesson-overview-panel');
  if (panel) panel.style.display = 'none';
}

async function openLessonOverview() {
  const panel = document.getElementById('lesson-overview-panel');
  if (!panel) return;
  panel.style.display = 'block';
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  const titleEl = document.getElementById('lesson-overview-title');
  const scopeEl = document.getElementById('lesson-overview-scope');
  const passagesEl = document.getElementById('lesson-overview-passages');
  const topicsEl = document.getElementById('lesson-overview-topics');

  if (titleEl && titleEl.textContent) return;

  try {
    const res = await fetch('/api/lesson/overview');
    const data = await res.json();
    if (!res.ok) throw new Error('Không tải được tổng quan bài học');

    if (titleEl) titleEl.textContent = data.title || 'Day 1: Khái niệm RAG';
    if (scopeEl) scopeEl.textContent = data.scope || '';

    if (passagesEl) {
      passagesEl.replaceChildren();
      (data.key_passages || []).forEach(p => {
        const item = document.createElement('div');
        item.style.cssText = 'padding: 10px 14px; background: var(--bg-subtle, #f8fafc); border-left: 3px solid #000; font-size: 13px; line-height: 1.5; color: #1e293b;';
        item.innerHTML = `<strong style="font-family: monospace; color: #0f172a;">[${p.id}]</strong> ${p.text}...`;
        passagesEl.appendChild(item);
      });
    }

    if (topicsEl) {
      topicsEl.replaceChildren();
      (data.question_topics || []).forEach(t => {
        const tag = document.createElement('span');
        tag.className = 'institutional-badge';
        tag.style.cssText = 'background: #f1f5f9; border: 1px solid #000; color: #0f172a; padding: 4px 10px; font-size: 12px; font-weight: 600;';
        tag.textContent = `🎯 ${t.concept} (${t.type === 'multiple_choice' ? 'Trắc nghiệm' : 'Tự luận'})`;
        topicsEl.appendChild(tag);
      });
    }
  } catch (err) {
    console.warn(err);
  }
}

window.addEventListener('DOMContentLoaded', async () => {
  const isInstructorPage = window.location.pathname.includes('/instructor') || window.location.pathname.includes('/teacher');
  const sessionId = localStorage.getItem('vlearn_session_id');
  const role = localStorage.getItem('vlearn_role');
  const displayName = localStorage.getItem('vlearn_display_name');

  if (!sessionId || !role) {
    const authGate = document.getElementById('auth-gate');
    if (authGate) authGate.style.display = 'grid';
    switchAuthRole(isInstructorPage ? 'teacher' : 'student');
    return;
  }

  learningSessionId = sessionId;
  if (role === 'student') {
    showStudentWorkspace(displayName || 'Học viên');
  } else if (role === 'teacher') {
    showTeacherWorkspace(displayName || 'Giảng viên');
    try { await loadInstructorReport(); } catch (err) { console.warn(err); switchAccount(); }
  }
});
