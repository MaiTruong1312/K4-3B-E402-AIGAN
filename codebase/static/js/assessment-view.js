function updateSupportProgress(ai = null) {
  if (ai && Number(ai.attempt_number)) currentAttemptNumber = Number(ai.attempt_number);
  const stage = currentAttemptNumber >= 3 ? 3 : Math.max(1, currentAttemptNumber || 1);
  document.querySelectorAll('.attempt-indicator').forEach(element => {
    element.textContent = currentAttemptNumber ? `Lần thử ${currentAttemptNumber} · Tầng ${stage}` : 'Chưa bắt đầu';
  });
  document.querySelectorAll('.support-policy-step').forEach(element => {
    const step = Number(element.dataset.supportStep);
    element.classList.toggle('active', step === stage);
    element.classList.toggle('done', currentAttemptNumber > 0 && step < stage);
  });
}

function showRevealedAnswer(ai) {
  const card = document.getElementById('revealed-answer-card');
  if (!card) return;
  if (!ai || !ai.reveal_answer) {
    card.style.display = 'none';
    return;
  }
  const answer = ai.revealed_correct_option;
  document.getElementById('revealed-answer-title').textContent = answer
    ? `Đáp án phù hợp nhất: ${answer.id}. ${answer.text}`
    : 'Lời giải định hướng đã được mở sau nhiều lần thử.';
  document.getElementById('revealed-answer-description').textContent = answer
    ? 'Hãy dùng đáp án đã mở làm căn cứ để tự giải thích lại; chỉ chọn đúng chưa được tính là đã hiểu.'
    : (ai.hint_level_2 || ai.explanation || '');
  card.style.display = 'block';
}

function renderLearningRoute(ai) {
  const card = document.getElementById('learning-route-card');
  const container = document.getElementById('learning-route-sources');
  if (!card || !container) return;
  const sources = ai?.learning_route?.sources || [];
  container.replaceChildren();
  if (!sources.length) {
    card.style.display = 'none';
    return;
  }
  sources.forEach(source => {
    const item = document.createElement('div');
    item.className = 'learning-route-source';
    const id = document.createElement('strong');
    id.textContent = `${source.id} · ${source.file || 'Transcript VLearn'}`;
    const text = document.createElement('span');
    text.textContent = source.text;
    item.append(id, text);
    container.appendChild(item);
  });
  card.style.display = 'block';
}

function assessmentHeading(ai) {
  const headings = {
    PARTIAL: 'Bạn đã đúng một phần, nhưng còn thiếu một mắt xích quan trọng',
    MIXED: 'Lập luận đang có cả ý đúng và một ý cần sửa',
    CONTRADICTION: 'Hai ý trong phần giải thích đang mâu thuẫn nhau',
    SELECTION_MISMATCH: 'Lập luận và phương án bạn chọn chưa khớp nhau',
    COPYING: 'Chưa đủ bằng chứng rằng bạn đã tự diễn đạt cách hiểu',
    QUESTION_DEFECT: 'Câu hỏi này cần được giảng viên kiểm tra lại',
    MISCONCEPTION: `Có một giả định cần kiểm tra lại trong phần ${activeQuestionConcept || 'lập luận'}`
  };
  return headings[ai.assessment_type] || headings.MISCONCEPTION;
}
