import java.util.*;

class NumberTracker {
	private Set<Integer> remaining;
	
	public void reset() {
		remaining = new HashSet<Integer>();
		
		for (int i = 1; i <= 9; i++) {
			remaining.add(i);
		}
	}
	
	public boolean removeNum(int num) {
		return remaining.remove(num);
	}
}

public class SudokuValidator {
    public static boolean check(int[][] sudoku) {
		NumberTracker numberTracker = new NumberTracker();
        int i, j, k, l;
        
		// rows
        for (i = 0; i < 9; i++) {
			numberTracker.reset();
			for (j = 0; j < 9; j++) {
				if (!numberTracker.removeNum(sudoku[i][j])) {
					return false;
				}
			}
		}
		
		// columns
		for (i = 0; i < 9; i++) {
			numberTracker.reset();
			for (j = 0; j < 9; j++) {
				if (!numberTracker.removeNum(sudoku[i][j])) {
					return false;
				}
			}
		}
		
		// 3x3 squares
		for (i = 0; i < 3; i++) {
			for (j = 0; j < 3; j++) {
				numberTracker.reset();
				for (k = 0; k < 3; k++) {
					for (l = 0; l < 3; l++) {
						if (!numberTracker.removeNum(sudoku[i * 3 + k][j * 3 + l])) {
							return false;
						}
					}
				}
			}
		}
		
		return true;
    }
}