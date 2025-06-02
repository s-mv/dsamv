class IsUnique {
  constructor() {
    this.tests = {
      "you shall not pass": false,
      "you can": true,
      "you cannot": false,
      "maybe no?": true
    };
  }

  static solution = (input) => {
    const seen = [];
    for (let i = 0; i < input.length; i++) {
      if (seen.includes(input[i])) {
        return false;
      }
      seen.push(input[i]);
    }
    return true;
  }

  runTests = () => {
    for (const [input, expected] of Object.entries(this.tests)) {
      const result = IsUnique.solution(input);
      console.log(`Running input "${input}" -> ${result === expected ? "PASSED" : "FAILED"}`);
    }
  }
}

const tester = new IsUnique();
tester.runTests();
