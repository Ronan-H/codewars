const beats = {
  rock: 'scissors',
  scissors: 'paper',
  paper: 'rock',
};

const rps = (p1, p2) => {
  if (p1 === p2) {
    return 'Draw!';
  }
  
  return `Player ${beats[p1] === p2 ? '1' : '2'} won!`;
};
