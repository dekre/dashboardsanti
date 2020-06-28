export function addLeadingZero(numericString: string) {
  var res = numericString;
  if (numericString.length < 2) {
    res = '0' + numericString;
  }
  return res;
}

export function getCurrentTimestamp() {
  const date = new Date()
  const Y = date.getFullYear();
  const M = addLeadingZero('' + date.getMonth());
  const D = addLeadingZero('' + date.getDate());
  const h = addLeadingZero('' + date.getHours());
  const m = addLeadingZero('' + date.getMinutes());
  const s = addLeadingZero('' + date.getSeconds());
  return Y + '-' + M + '-' + D + ' ' + h + ':' + m + ':' + s;  
}
