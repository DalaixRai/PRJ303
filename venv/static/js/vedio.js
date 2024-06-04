document.addEventListener("DOMContentLoaded", function () {
  const videoWrapper = document.querySelector(".video-wrapper");
  const video = videoWrapper.querySelector("video");
  const playPauseButton = document.querySelector(".play-pause-button");
  const videoTime = document.querySelector(".video-time");
  const videoProgress = document.querySelector(".video-progress");
  const fullscreenButton = document.querySelector(".fullscreen-button");

  video.addEventListener("timeupdate", updateTime);
  playPauseButton.addEventListener("click", togglePlayPause);
  videoProgress.addEventListener("input", handleProgress);
  fullscreenButton.addEventListener("click", toggleFullscreen);

  function updateTime() {
    const currentTime = formatTime(video.currentTime);
    const duration = formatTime(video.duration);
    videoTime.textContent = `${currentTime} / ${duration}`;
    videoProgress.value = (video.currentTime / video.duration) * 100;
  }

  function formatTime(time) {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${padZero(minutes)}:${padZero(seconds)}`;
  }

  function padZero(num) {
    return num < 10 ? `0${num}` : num;
  }

  function togglePlayPause() {
    if (video.paused) {
      video.play();
      playPauseButton.classList.add("playing");
    } else {
      video.pause();
      playPauseButton.classList.remove("playing");
    }
  }

  function handleProgress() {
    const value = videoProgress.value;
    video.currentTime = (value / 100) * video.duration;
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      videoWrapper.requestFullscreen().catch(err => {
        alert(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
      });
    } else {
      document.exitFullscreen();
    }
  }
});
