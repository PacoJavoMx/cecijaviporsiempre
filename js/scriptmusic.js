let isPlaying = false;

window.addEventListener('DOMContentLoaded', () => {
  const audio = document.getElementById('bg-music');
  const icon = document.querySelector('#music-btn i');

  // Crear el círculo de progreso dinámicamente
  const progress = document.createElement('div');
  progress.id = 'music-progress';
  document.getElementById('music-player').appendChild(progress);

  // Intentar autoplay
  audio.play().then(() => {
    isPlaying = true;
    icon.className = 'fas fa-pause';
  }).catch(() => {
    isPlaying = false;
    icon.className = 'fas fa-play';

    // Activar música en el primer clic (especial para móviles)
    window.addEventListener('click', () => {
      if (!isPlaying) {
        audio.play().then(() => {
          isPlaying = true;
          icon.className = 'fas fa-pause';
        });
      }
    }, { once: true });
  });

  // Alternar reproducción con el botón
  document.getElementById('music-btn').addEventListener('click', () => {
    if (isPlaying) {
      audio.pause();
      icon.className = 'fas fa-play';
    } else {
      audio.play();
      icon.className = 'fas fa-pause';
    }
    isPlaying = !isPlaying;
  });

  // Actualizar solo el borde circular (aro)
  audio.addEventListener('timeupdate', () => {
    if (audio.duration) {
      const percent = (audio.currentTime / audio.duration) * 100;
      progress.style.setProperty('--progress', `${percent}%`);
    }
  });
});
