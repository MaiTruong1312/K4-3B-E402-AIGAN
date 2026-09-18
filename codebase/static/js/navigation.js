function switchMainView(mode) {
  const interactiveView = document.getElementById('interactive-view');
  const diagramView = document.getElementById('diagram-view');
  const stepNavBar = document.getElementById('step-nav-bar');
  const btnInteractive = document.getElementById('btn-mode-interactive');
  const btnDiagram = document.getElementById('btn-mode-diagram');
  const showingDiagram = mode === 'diagram';
  interactiveView.style.display = showingDiagram ? 'none' : 'block';
  diagramView.style.display = showingDiagram ? 'block' : 'none';
  stepNavBar.style.display = showingDiagram ? 'none' : 'flex';
  btnDiagram.classList.toggle('active', showingDiagram);
  btnInteractive.classList.toggle('active', !showingDiagram);
  if (!showingDiagram) goToStep(currentStep);
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
