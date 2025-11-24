function sumArray(arr) {
  if (!Array.isArray(arr) || arr.length < 2) {
    return 0;
  }
  
  return arr.sort((a, b) => b - a).slice(1, arr.length - 1).reduce((a, b) => a + b, 0);
}
