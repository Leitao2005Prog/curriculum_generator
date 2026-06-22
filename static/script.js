function copyEmailToClipboard(button) {
  // Recupera o e-mail guardado no atributo data-email
  const email = button.getAttribute('data-email');
  // Encontra o span de feedback que está logo ao lado do botão
  const feedback = button.nextElementSibling;

  if (!email) return;

  // Usa a API moderna de área de transferência
  navigator.clipboard.writeText(email).then(() => {
    if (feedback) {
      feedback.textContent = " — Copiado!";
      button.style.display = "none"; // Esconde o botão temporariamente

      // Reseta o estado após 2.5 segundos
      setTimeout(() => {
        feedback.textContent = "";
        button.style.display = "inline-block";
      }, 2500);
    }
  }).catch(err => {
    console.error("Erro ao copiar e-mail: ", err);
    // Fallback simples caso o navegador bloqueie a API por segurança
    feedback.textContent = " — Erro ao copiar. Selecione o texto.";
  });
}