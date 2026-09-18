async function ensureLearningSession() {
  if (learningSessionId) return learningSessionId;
  throw new Error('Bạn cần đăng nhập bằng mã sinh viên trước khi làm bài');
}

async function analyzeWithAI(questionId, answer, reasoning, stage = 'initial') {
  const sessionId = await ensureLearningSession();
  const requestId = crypto.randomUUID();
  const response = await fetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      request_id: requestId,
      question_id: questionId,
      selected_answer: answer,
      reasoning,
      stage
    })
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || 'AI chưa phản hồi được');
  backendMode = data.mode || 'live';
  return data;
}

async function saveLearningAttempt(stage, question, reasoning) {
  if (!learningSessionId) return;
  try {
    await fetch('/api/attempt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: learningSessionId, stage, question, reasoning })
    });
  } catch (error) {
    console.warn('Không lưu được attempt', error);
  }
}
