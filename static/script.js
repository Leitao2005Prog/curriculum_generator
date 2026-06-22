function copyEmailToClipboard(button) {
      const email = button.getAttribute('data-email');
      const feedback = button.nextElementSibling;

      if (!email) return;

      navigator.clipboard.writeText(email).then(() => {
        if (feedback) {
          feedback.textContent = " — Copiado!";
          button.style.display = "none";

          setTimeout(() => {
            feedback.textContent = "";
            button.style.display = "inline-block";
          }, 2500);
        }
      }).catch(err => {
        console.error("Erro ao copiar e-mail: ", err);
        feedback.textContent = " — Erro ao copiar.";
      });
    }

      function copyPhoneToClipboard(button) {
    var phone = button.getAttribute('data-phone');
    var feedback = button.nextElementSibling;

    function showFeedback(message) {
      if (feedback) {
        feedback.textContent = message;
        setTimeout(function () { feedback.textContent = ''; }, 2000);
      }
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(phone).then(function () {
        showFeedback('copiado!');
      }).catch(function () {
        showFeedback('não foi possível copiar — selecione o texto manualmente');
      });
    } else {
      showFeedback('selecione o texto manualmente para copiar');
    }
  }