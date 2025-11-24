function cookie(x){
  const getName = (obj) => {
    switch (typeof x) {
      case 'string':
        return 'Zach';
      case 'number':
        return 'Monica';
      default:
        return 'the dog';
    }
  };
  
  return `Who ate the last cookie? It was ${getName()}!`;
}
