function copiarCLABE(event) {
    event.preventDefault(); // Previene el comportamiento por defecto del enlace
  
    const clabeTexto = document.getElementById("clabe").textContent;
    const clabeSoloNumeros = clabeTexto.replace("CLABE: ", "").trim();
  
    navigator.clipboard.writeText(clabeSoloNumeros).then(() => {
      Swal.fire({
        title: '¡CLABE copiada!',
        text: 'Ya puedes pegarla en tu app bancaria.',
        icon: 'success',
        timer: 3000,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
      });
    }).catch(err => {
      Swal.fire({
        title: 'Ups...',
        text: 'No se pudo copiar la CLABE.',
        icon: 'error',
        confirmButtonText: 'Ok'
      });
      console.error('Error al copiar:', err);
    });
  }
  