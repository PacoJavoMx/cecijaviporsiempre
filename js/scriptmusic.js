let isPlaying = false;

window.addEventListener('DOMContentLoaded', () => {
  const audio = document.getElementById('bg-music');
  const icon = document.querySelector('#music-btn i');

  // Intentar autoplay
  audio.play().then(() => {
    isPlaying = true;
    icon.className = 'fas fa-pause';
  }).catch(() => {
    isPlaying = false;
    icon.className = 'fas fa-play';

    // Reproducir en el primer clic en cualquier parte del documento
    window.addEventListener('click', () => {
      if (!isPlaying) {
        audio.play().then(() => {
          isPlaying = true;
          icon.className = 'fas fa-pause';
        });
      }
    }, { once: true });
  });

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
});
