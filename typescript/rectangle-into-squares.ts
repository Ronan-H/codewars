
export function sqInRect(l: number, w: number): null | number[] {
    if (l === w) {
      return null;
    }
  
    // Calculate the biggest square we can make out of this rect,
    // and the length of the remaining rect.
    const square = Math.abs(l - w);
    const rem = Math.min(l, w);
  
    // Find the rest of the sequence by recursively completing the above step.
    const next = sqInRect(square, rem);
 
  
    // Finding a square (null) indicates the end of a sequence.
    // Otherwise, we concatenate the result with the rest of the sequence here.
    return next === null ? [rem, rem] : [rem, ...next];
}
