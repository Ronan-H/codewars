export function isPalindrome(x: string): boolean {
  const lower = x.toLowerCase();
  
  for (let i = 0; i < lower.length / 2; i++) {
    if (lower[i] !== lower[lower.length - i - 1]) {
      return false;
    }
  }
  
  return true;
}
