function switchAuthRole(role) {
  const isStudent = role === 'student';
  document.getElementById('student-login-form').style.display = isStudent ? 'block' : 'none';
  document.getElementById('teacher-login-form').style.display = isStudent ? 'none' : 'block';
  document.getElementById('auth-tab-student').classList.toggle('active', isStudent);
  document.getElementById('auth-tab-teacher').classList.toggle('active', !isStudent);
  document.getElementById('auth-error').textContent = '';
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

function showStudentWorkspace(displayName) {
  document.getElementById('auth-gate').style.display = 'none';
  document.getElementById('instructor-panel').style.display = 'none';
  document.querySelector('main.container').style.display = '';
  const avatar = document.getElementById('current-user-avatar');
  avatar.textContent = displayName.slice(0, 2).toUpperCase();
  avatar.title = `Học viên: ${displayName}`;
  document.getElementById('student-welcome-title').textContent = `Chào bạn, học viên ${displayName}!`;
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
    document.getElementById('auth-gate').style.display = 'none';
    document.querySelector('main.container').style.display = 'none';
    document.getElementById('instructor-panel').style.display = 'block';
    await loadInstructorReport();
  } catch (error) {
    document.getElementById('auth-error').textContent = error.message;
  }
}

async function loadInstructorReport() {
  const response = await fetch(`/api/instructor/report?session_id=${encodeURIComponent(learningSessionId)}`);
  const report = await response.json();
  if (!response.ok) throw new Error(report.detail || 'Không tải được báo cáo');
  const root = document.getElementById('instructor-report-content');
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
  document.getElementById('instructor-panel').style.display = 'none';
  document.querySelector('main.container').style.display = '';
  document.getElementById('auth-gate').style.display = 'grid';
  document.getElementById('student-login-form').reset();
  document.getElementById('teacher-login-form').reset();
  switchAuthRole('student');
}

window.addEventListener('DOMContentLoaded', async () => {
  const sessionId = localStorage.getItem('vlearn_session_id');
  const role = localStorage.getItem('vlearn_role');
  const displayName = localStorage.getItem('vlearn_display_name');
  if (!sessionId || !role) return;
  learningSessionId = sessionId;
  if (role === 'student') showStudentWorkspace(displayName || 'Học viên');
  if (role === 'teacher') {
    document.getElementById('auth-gate').style.display = 'none';
    document.querySelector('main.container').style.display = 'none';
    document.getElementById('instructor-panel').style.display = 'block';
    try { await loadInstructorReport(); } catch (_) { logoutUser(); }
  }
});
