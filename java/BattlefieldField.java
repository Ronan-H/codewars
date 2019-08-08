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
    }
}