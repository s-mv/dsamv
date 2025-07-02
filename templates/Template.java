package templates; /* REPLACE WITH type.java -> Example: arrays.java */

import helpers.Helper;

/* 
 * To the Java... users. Uh.
 *
 * This cost me my sanity.
 * But here it is, a template for Java.
 *
 * REPLACE Solution.solution with your solution.
 *
 * Respct,
 * smv.
 */

class Solution {
  public float solution(int a) {
    return 0.f;
  }

  /*** EVERYTHING AFTER THIS CAN BE AVOIDED ***/

  public static void main(String[] args) {
    if (args.length == 0) {
      System.err.println("Usage: <path-to-test-file>");
      return;
    }

    Helper.test(new Solution(), args[0]);
  }
}

public class Template {
  public static void main(String[] args) {
    Solution.main(args);
  }
}