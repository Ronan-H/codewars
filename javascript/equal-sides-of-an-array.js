function findEvenIndex(arr)
{
  var leftSum = 0;
  var rightSum = 0;

  for (var i = 1; i < arr.length; i++) {
    rightSum += arr[i];
  }
  
  for (var i = 0; i < arr.length; i++) {
    if (leftSum == rightSum) {
      return i;
    }
    
    leftSum += arr[i];
    rightSum -= arr[i + 1];
  }
  
  return -1;
}
