function spinWords(str){
  return str.split(' ').map(word => word.length < 5 ? word : word.split('').reverse().join('')).join(' ');
}
