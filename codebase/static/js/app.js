let currentQuestionIdx = 0; // 0 = Question 1, 1 = Question 2
    let currentStep = 1;
    let activeQuestion = '';
    let activeQuestionId = '';
    let activeQuestionConcept = '';
    let selectedChoice = null;
    let learningSessionId = null;
    let backendMode = 'live';
    let currentCitationSources = [];
    let lessonQuestions = [];
    let activeQuestionFilter = 'all';
    let loadingTimer = null;
    let currentAttemptNumber = 0;

    const loadingMessages = [
      'Đang đọc cách bạn suy luận...',
      'Đang tạo rubric riêng cho câu hỏi này...',
      'Đang đối chiếu từng giả định với tài liệu bài học...',
      'Đang chọn gợi ý vừa đủ để bạn vẫn phải tự suy nghĩ...',
      'Đang kiểm tra nguồn trích dẫn trước khi phản hồi...'
    ];

    function setLoading(isLoading) {
      const overlay = document.getElementById('ai-loading');
      const message = document.getElementById('ai-loading-message');
      const buttons = [
        document.getElementById('btn-submit-answer'),
        document.getElementById('btn-verify-retry')
      ].filter(Boolean);
      buttons.forEach(button => { button.disabled = isLoading; });
      clearInterval(loadingTimer);
      loadingTimer = null;
      if (!isLoading) {
        overlay.classList.remove('open');
        document.body.style.overflow = '';
        return;
      }
      let messageIndex = 0;
      message.textContent = loadingMessages[messageIndex];
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      loadingTimer = setInterval(() => {
        messageIndex = (messageIndex + 1) % loadingMessages.length;
        message.textContent = loadingMessages[messageIndex];
      }, 1800);
    }

    async function loadLesson() {
      const response = await fetch('/api/lesson');
      if (!response.ok) throw new Error('Không tải được nội dung bài học');
      const lesson = await response.json();
      lessonQuestions = lesson.questions || [];
      if (!lessonQuestions.length) throw new Error('Bài học chưa có câu hỏi');
      document.getElementById('count-all').textContent = lessonQuestions.length;
      document.getElementById('count-essay').textContent = lessonQuestions.filter(question => question.type === 'essay').length;
      document.getElementById('count-mcq').textContent = lessonQuestions.filter(question => question.type === 'multiple_choice').length;
      renderQuestionBrowser();
      const finalCount = document.getElementById('final-question-count');
      if (finalCount) finalCount.textContent = `${lessonQuestions.length} / ${lessonQuestions.length} câu hỏi`;
      return lesson;
    }

    function renderCitationSources(sources) {
      const list = document.getElementById('citation-list');
      list.replaceChildren();
      if (!sources.length) {
        const empty = document.createElement('p');
        empty.className = 'citation-text';
        empty.textContent = 'Chưa có đoạn nguồn nào được gắn với lần phân tích này.';
        list.appendChild(empty);
        return;
      }
      sources.forEach(source => {
        const item = document.createElement('article');
        item.className = 'citation-item';
        const id = document.createElement('div');
        id.className = 'citation-id';
        id.textContent = source.id;
        const text = document.createElement('div');
        text.className = 'citation-text';
        text.textContent = source.text;
        item.append(id, text);
        list.appendChild(item);
      });
    }

    async function openCitationModal() {
      const modal = document.getElementById('citation-modal');
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (!currentCitationSources.length) {
        try {
          const response = await fetch('/api/sources');
          if (!response.ok) throw new Error('Không tải được nguồn');
          currentCitationSources = (await response.json()).sources || [];
        } catch (error) {
          console.warn(error);
        }
      }
      renderCitationSources(currentCitationSources);
    }

    function closeCitationModal(event) {
      if (event && event.target !== event.currentTarget) return;
      document.getElementById('citation-modal').classList.remove('open');
      document.body.style.overflow = '';
    }

    function renderQuestionBrowser() {
      const container = document.getElementById('question-jump-list');
      if (!container) return;
      container.replaceChildren();
      lessonQuestions.forEach((question, index) => {
        if (activeQuestionFilter !== 'all' && question.type !== activeQuestionFilter) return;
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'question-jump-btn';
        button.classList.toggle('active', index === currentQuestionIdx);
        button.innerHTML = `Câu ${index + 1}<span class="question-kind">${question.type === 'essay' ? 'Tự luận' : 'Trắc nghiệm'}</span>`;
        button.addEventListener('click', () => renderQuestion(index));
        container.appendChild(button);
      });
    }

    // Load a teacher-authored question from the lesson; the learner answers freely.
    function renderQuestion(idx) {
      if (!lessonQuestions.length) return;
      currentQuestionIdx = idx;
      const question = lessonQuestions[idx] || lessonQuestions[0];
      activeQuestion = question.text;
      activeQuestionId = question.id;
      activeQuestionConcept = question.concept;
      selectedChoice = null;
      currentAttemptNumber = 0;
      updateSupportProgress();
      showRevealedAnswer(null);
      document.getElementById('quiz-step-tag').textContent = `BƯỚC II / V · CÂU HỎI ${idx + 1} / ${lessonQuestions.length}`;
      document.getElementById('quiz-breadcrumb-tag').textContent = question.concept;
      document.getElementById('quiz-progress-badge').textContent = `Tiến độ: Câu ${idx + 1} / ${lessonQuestions.length}`;
      document.getElementById('question-concept-tag').textContent = `Khái niệm: ${question.concept}`;
      document.getElementById('lesson-question-text').textContent = question.text;
      renderChoices(question);
      renderQuestionBrowser();
      document.getElementById('user-explanation').value = '';
    }

    function renderChoices(question) {
      const section = document.getElementById('multiple-choice-section');
      const container = document.getElementById('dynamic-choice-container');
      const retrySection = document.getElementById('retry-choice-section');
      const retryContainer = document.getElementById('retry-choice-container');
      container.replaceChildren();
      retryContainer.replaceChildren();
      if (question.type !== 'multiple_choice') {
        section.style.display = 'none';
        retrySection.style.display = 'none';
        return;
      }
      section.style.display = 'block';
      retrySection.style.display = 'block';
      renderChoiceSet(container, question.options || []);
      renderChoiceSet(retryContainer, question.options || []);
    }

    function renderChoiceSet(container, options) {
      options.forEach(option => {
        const item = document.createElement('button');
        item.type = 'button';
        item.className = 'choice-item';
        item.dataset.optionId = option.id;
        const letter = document.createElement('span');
        letter.className = 'choice-letter';
        letter.textContent = option.id;
        const content = document.createElement('span');
        content.className = 'choice-content';
        content.textContent = option.text;
        item.append(letter, content);
        item.addEventListener('click', () => {
          selectedChoice = option.id;
          document.querySelectorAll('#dynamic-choice-container .choice-item, #retry-choice-container .choice-item').forEach(choice => {
            choice.classList.toggle('selected', choice.dataset.optionId === option.id);
          });
        });
        container.appendChild(item);
      });
    }

    // Submit Step 2 & Check Right/Wrong
    async function submitStep2() {
      const question = activeQuestion;
      const text = document.getElementById('user-explanation').value.trim();

      const elCorrect = document.getElementById('ai-result-correct');
      const elSuff = document.getElementById('ai-result-sufficient');
      const elInsuff = document.getElementById('ai-result-insufficient');

      if (!question) {
        alert('Câu hỏi bài học chưa tải xong. Vui lòng thử lại.');
        return;
      }
      const activeConfig = lessonQuestions[currentQuestionIdx];
      if (activeConfig.type === 'multiple_choice' && !selectedChoice) {
        alert('Hãy chọn một phương án trước khi gửi.');
        return;
      }
      if (!text) {
        alert('Hãy viết cách hiểu hiện tại của bạn trước khi gửi.');
        return;
      }
      try {
        setLoading(true);
        const ai = await analyzeWithAI(activeQuestionId, selectedChoice, text);
        updateSupportProgress(ai);
        showRevealedAnswer(ai);
        renderLearningRoute(ai);
        currentCitationSources = ai.sources || [];

        if (ai.decision === 'CLARIFY' || ai.decision === 'DECLINE') {
          elCorrect.style.display = 'none';
          elSuff.style.display = 'none';
          elInsuff.style.display = 'block';
          document.getElementById('clarify-text').textContent = ai.clarifying_question || ai.explanation;
        } else if (ai.decision === 'VERIFY') {
          elCorrect.style.display = 'block';
          elSuff.style.display = 'none';
          elInsuff.style.display = 'none';
          document.getElementById('correct-feedback-desc').textContent = `${ai.explanation} Hệ thống sẽ dùng câu tiếp theo để kiểm tra bạn hiểu thật hay chỉ chọn đúng.`;
          document.getElementById('correct-source-tag').textContent = `Nguồn: ${(ai.source_ids || []).join(', ')} · ${backendMode.toUpperCase()}`;
          const nextBtn = document.getElementById('btn-next-q-from-correct');
          nextBtn.textContent = currentQuestionIdx < lessonQuestions.length - 1 ? 'Qua câu tiếp theo →' : 'Hoàn thành & Xem tổng kết →';
        } else {
          elCorrect.style.display = 'none';
          elSuff.style.display = 'block';
          elInsuff.style.display = 'none';
          document.getElementById('wrong-detected-title').textContent = assessmentHeading(ai);
          document.getElementById('wrong-user-summary').textContent = ai.evidence_from_student
            ? `AI đang tập trung vào ý bạn vừa viết: “${ai.evidence_from_student}”`
            : (ai.explanation || 'Chưa đủ bằng chứng để xác nhận hoàn thành.');
          document.getElementById('minimal-hint-text').textContent = ai.hint_level_1;
          document.getElementById('hint-source-text').textContent = `Nguồn: ${(ai.source_ids || []).join(', ')} · Confidence ${Math.round((ai.confidence || 0) * 100)}% · ${backendMode.toUpperCase()}`;
          document.getElementById('retry-hint-display').innerHTML = `<em>"${ai.hint_level_1}"</em>`;
          document.getElementById('retry-explanation').value = '';
          document.getElementById('retry-success-box').style.display = 'none';
          document.getElementById('retry-next-container').style.display = 'none';
          document.getElementById('btn-verify-retry').style.display = 'inline-flex';
        }
        goToStep(3);
        return;
      } catch (error) {
        console.error('Không phân tích được câu trả lời:', error);
        alert(`Chưa thể phân tích bằng AI: ${error.message}. Vui lòng kiểm tra backend rồi thử lại.`);
        return;
      } finally {
        setLoading(false);
      }
    }

    // Submit Step 4 (Retry)
    async function submitRetry() {
      const retryText = document.getElementById('retry-explanation').value.trim();

      if (retryText.length < 15) {
        alert('Hãy giải thích lại bằng ít nhất một câu đầy đủ.');
        return;
      }

      try {
        setLoading(true);
        const ai = await analyzeWithAI(activeQuestionId, selectedChoice, retryText, 'retry');
        updateSupportProgress(ai);
        showRevealedAnswer(ai);
        renderLearningRoute(ai);
        if (ai.decision !== 'VERIFY') {
          const box = document.getElementById('retry-success-box');
          box.style.display = 'block';
          const badge = box.querySelector('.result-badge');
          const title = box.querySelector('.result-title');
          const description = box.querySelector('.result-desc');
          if (ai.reveal_answer) {
            badge.textContent = 'TẦNG HỖ TRỢ 3 · ĐÃ MỞ ĐÁP ÁN';
            title.textContent = `Bạn đã thử ${ai.attempt_number} lần. Hệ thống mở đáp án và căn cứ để bạn không bị mắc kẹt.`;
            description.textContent = 'Xem khối đáp án phía trên, chọn lại nếu cần, rồi giải thích vì sao bằng lời của bạn.';
          } else {
            badge.textContent = ai.attempt_number >= 3 ? 'ĐANG NÂNG MỨC HỖ TRỢ' : 'CHƯA ĐỦ BẰNG CHỨNG ĐÃ HIỂU';
            title.textContent = ai.attempt_number >= 3
              ? `Đây là lần thử ${ai.attempt_number}; hệ thống đã chuyển sang gợi ý theo từng bước.`
              : ai.explanation;
            description.textContent = ai.clarifying_question || ai.hint_level_1 || ai.explanation || '';
          }
          const nextHint = ai.hint_level_1 || ai.clarifying_question;
          if (nextHint) document.getElementById('retry-hint-display').textContent = nextHint;
          document.getElementById('retry-next-container').style.display = 'none';
          return;
        }
      } catch (error) {
        console.error('Không đánh giá được lần sửa bằng backend:', error);
        alert(`Chưa thể xác nhận lần sửa bằng AI: ${error.message}. Vui lòng thử lại.`);
        return;
      } finally {
        setLoading(false);
      }

      // Update final comparison in Step 5
      if (currentQuestionIdx === 0) {
        const finalAfter1 = document.getElementById('final-after-text-1');
        if (finalAfter1 && retryText) {
          finalAfter1.innerHTML = `<em>"${retryText}"</em>`;
        }
      } else {
        const finalAfter2 = document.getElementById('final-after-text-2');
        if (finalAfter2 && retryText) {
          finalAfter2.innerHTML = `Đã hiểu đúng: <em>"${retryText}"</em>`;
        }
      }

      // Show success notification on screen 4
      document.getElementById('retry-success-box').style.display = 'block';
      const successBox = document.getElementById('retry-success-box');
      successBox.querySelector('.result-badge').textContent = 'CÓ BẰNG CHỨNG BAN ĐẦU ĐÃ TỰ SỬA';
      successBox.querySelector('.result-title').textContent = 'Cách giải thích mới đã vượt qua rubric của bài luyện.';
      successBox.querySelector('.result-desc').textContent = 'Kết quả này chưa phải điểm số chính thức; câu tiếp theo dùng để kiểm tra khả năng chuyển giao.';
      document.getElementById('btn-verify-retry').style.display = 'none';

      const nextContainer = document.getElementById('retry-next-container');
      const nextBtn = document.getElementById('btn-next-q-from-retry');
      nextContainer.style.display = 'block';

      if (currentQuestionIdx < lessonQuestions.length - 1) {
        nextBtn.textContent = "Qua câu tiếp theo →";
      } else {
        nextBtn.textContent = "Hoàn thành bài luyện tập & Xem tổng kết →";
      }
    }

    // Transition to Next Question or Final Step
    function goToNextQuestion() {
      if (currentQuestionIdx < lessonQuestions.length - 1) {
        renderQuestion(currentQuestionIdx + 1);
        goToStep(2);
      } else {
        // Finished both questions -> Move to Step 5
        goToStep(5);
      }
    }

    // Restart Quiz helpers
    function restartQuiz() {
      renderQuestion(0);
      goToStep(1);
    }

    function restartQuizToQ1() {
      renderQuestion(0);
      goToStep(2);
    }

    // Default init on page load
    window.addEventListener('DOMContentLoaded', async () => {
      try {
        await loadLesson();
        renderQuestion(0);
      } catch (error) {
        console.error(error);
        document.getElementById('lesson-question-text').textContent = 'Không tải được câu hỏi. Hãy kiểm tra backend và tải lại trang.';
      }
    });
    window.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeCitationModal();
    });
  
