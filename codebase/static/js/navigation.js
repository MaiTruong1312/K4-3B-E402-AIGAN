function switchMainView(mode) {
  const interactiveView = document.getElementById('interactive-view');
  const diagramView = document.getElementById('diagram-view');
  const stepNavBar = document.getElementById('step-nav-bar');
  const instructorPanel = document.getElementById('instructor-panel');
  const btnInteractive = document.getElementById('btn-mode-interactive');
  const btnDiagram = document.getElementById('btn-mode-diagram');
  const showingDiagram = mode === 'diagram';
  const role = localStorage.getItem('vlearn_role');

  if (showingDiagram) {
    interactiveView.style.display = 'none';
    diagramView.style.display = 'block';
    stepNavBar.style.display = 'none';
    if (instructorPanel) instructorPanel.style.display = 'none';
  } else {
    diagramView.style.display = 'none';
    if (role === 'teacher') {
      interactiveView.style.display = 'none';
      stepNavBar.style.display = 'none';
      if (instructorPanel) instructorPanel.style.display = 'block';
    } else {
      interactiveView.style.display = 'block';
      stepNavBar.style.display = 'flex';
      if (instructorPanel) instructorPanel.style.display = 'none';
      goToStep(currentStep);
    }
  }

  btnDiagram.classList.toggle('active', showingDiagram);
  btnInteractive.classList.toggle('active', !showingDiagram);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goToStep(stepNum) {
  currentStep = stepNum;
  for (let index = 1; index <= 5; index += 1) {
    document.getElementById(`screen-${index}`)?.classList.toggle('active', index === stepNum);
    const pill = document.getElementById(`pill-step-${index}`);
    pill?.classList.toggle('active', index === stepNum);
    pill?.classList.toggle('done', index < stepNum);
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function filterQuestions(type) {
  activeQuestionFilter = type;
  document.querySelectorAll('.question-mode-btn').forEach(button => button.classList.remove('active'));
  document.getElementById(`mode-${type}`).classList.add('active');
  renderQuestionBrowser();
  const firstMatch = lessonQuestions.findIndex(question => type === 'all' || question.type === type);
  if (firstMatch >= 0) renderQuestion(firstMatch);
}
