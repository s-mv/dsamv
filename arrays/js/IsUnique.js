import Helper from "../../helpers/Helper.js";

class Solution {
  solution(input) {
    const seen = new Set();
    for (let i = 0; i < input.length; i++) {
      if (seen.has(input[i])) {
        return false;
      }
      seen.add(input[i]);
    }
    return true;
  }
}

Helper.test(new Solution());
