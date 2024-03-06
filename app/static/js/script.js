function formatInput(input) {
    // Converte para maiúsculas
    input.value = input.value.toUpperCase();
  
    // Remove todos os hífens existentes
    input.value = input.value.replace(/-/g, '');
  
    // Insere um hífen após o terceiro caractere, se necessário
    if (input.value.length > 3) {
      input.value = input.value.substring(0, 3) + '-' + input.value.substring(3);
    }
  }

  function upperCase(input) {
    input.value = input.value.toUpperCase();
  }
  