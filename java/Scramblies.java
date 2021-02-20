
public class Scramblies {
    public static boolean scramble(String s1, String s2) {
      int[] counts = new int[26];
      for (char c : s1.toCharArray()) counts[c - 97]++;
      for (char c : s2.toCharArray()) if (--counts[c - 97] < 0) return false;
      return true;
    }
}
