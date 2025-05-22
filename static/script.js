document.addEventListener('DOMContentLoaded', () => {
  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      // deactivate all
      document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
      // activate
      btn.classList.add('active');
      document.getElementById(`${btn.dataset.tab}-panel`).classList.add('active');
    });
  });

  // Show spinner on submit
  const form = document.getElementById('summaryForm');
  const submitBtn = document.getElementById('submitBtn');
  const spinner = submitBtn.querySelector('.loading-spinner');
  form.addEventListener('submit', () => {
    submitBtn.disabled = true;
    spinner.style.display = 'inline-block';
  });
});
