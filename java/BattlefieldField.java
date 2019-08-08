public class BattleField {

    public static boolean fieldValidator(int[][] field) {
        int i, j;

        // check for ships touching diagonally or adjacently
        for (i = 0; i < 9; i++) {
            for (j = 0; j < 9; j++) {
                if (field[i][j] == 1 && field[i + 1][j + 1] == 1
                 || field[i][j + 1] == 1 && field[i + 1][j] == 1) {
                    return false;
                }
            }
        }

        // count ships
        int[] shipCounts = new int[10];
        int cellCount;
        int magX, magY;
        int countX, countY;
        for (i = 0; i < 10; i++) {
            for (j = 0; j < 10; j++) {
                if (field[i][j] == 1) {
                    // ship found. check direction (either right or down)
                    if (i < 9 && field[i + 1][j] == 1) {
                        // ship going right
                        magX = 1;
                        magY = 0;
                    }
                    else {
                        // ship going down
                        magX = 0;
                        magY = 1;
                    }

                    // count ship cells
                    cellCount = 0;
                    countLoop:
                    for (countY = i; countY < 10; countY++) {
                        for (countX = j; countX < 10; countX++) {
                            if (field[countY][countX] == 0) {
                                break countLoop;
                            }

                            cellCount++;
                            field[countY][countX] = 0;
                        }
                    }

                    // add ship to ship count
                    shipCounts[cellCount]++;
                }
            }
        }

        // check that ship counts match the expected ships
        int[] expectedCounts = {0, 4, 3, 2, 1, 0, 0, 0, 0, 0};
        
        for (i = 0; i < 10; i++) {
            if (shipCounts[i] != expectedCounts[i]) {
                return false;
            }
        }

        return true;
    }
}