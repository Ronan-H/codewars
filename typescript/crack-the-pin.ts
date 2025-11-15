export function crack(targetHash: string): string {
  for (let n = 1; n <= 5; n++) {
    const gen = pinGenerator(n);
    let nextPin: string | null;
    
    while (nextPin = gen.next().value) {
      if (!nextPin) {
        break;
      }
      
      const hash = createHash("md5").update(nextPin).digest("hex");

      if (hash === targetHash) {
        return nextPin;
      }
    }
  }
  
  throw new Error("Didn't find the pin :(");
}

function* pinGenerator(len: number): Generator<string | null, string | null, void> {
  if (len === 1) {
    for (let i = 0; i < 10; i++) {
      yield i.toString();
    }
    
    return null;
  }

  const gen = pinGenerator(len - 1);
  let nextPin: string | null;
  
  while (nextPin = gen.next().value) {
    for (let i = 0; i < 10; i++) {
      yield (nextPin ?? '') + i.toString();
    }
  }
  
  return null;
}
