function addSeconds(date, seconds) {
  let oldDate = date;
  let addSeconds = seconds;
  var newSeconds = oldDate + addSeconds;
  //console.log(addSeconds);
  date.setSeconds(date.getSeconds() + seconds);
  return date;
}

export function showCountdownTimer() {
  //TODO rather than display a timer the whole time in a span, make it only show when there are e.g. 30 seconds left.
  // Maybe a whole page alert that the user will be logged out soon.

  // Get current date and time
  var now = new Date().getTime();
  let distance = countDownDate - now;
  // Output the result in an element with id="countdown-timer-span"
  let elementId = ("countdown-timer-span");
  document.getElementById(elementId).innerHTML = Math.floor(distance / 1000) + "s";

  // If the count down is over release resources
  if (distance < 0) {
    destroyCountdownTimer();
  }
}


// Set the date we're counting down to
let countDownDate = addSeconds(new Date(), 5);

let showTimerInterval = null;

export function destroyCountdownTimer() {
    clearInterval(showTimerInterval);
}

export function resetCountdownTimer(seconds) {
    destroyCountdownTimer(); // Destroy previous timer if any
    countDownDate = addSeconds(new Date(), seconds); // Set the date we're counting down to
    showTimerInterval = setInterval(showCountdownTimer, 1000); // Update the count down every 1 second
}