import fs from 'fs';

class Helper {
  static test(solutionInstance) {
    const filePath = process.argv[2];
    if (!filePath) {
      console.error('Usage: node <script> <test-file.json>');
      process.exit(1);
    }

    const testData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    let passed = 0;
    let total = 0;

    for (const { input, expected } of testData) {
      if (!Array.isArray(input)) {
        console.error('Error: Each "input" must be an array.');
        process.exit(1);
      }

      try {
        const result = solutionInstance.solution(...input);
        const ok = Helper.compareValues(result, expected);
        console.log(
          `Input: ${JSON.stringify(input)} => ${ok ? 'PASSED' : `FAILED (got ${JSON.stringify(result)}, expected ${JSON.stringify(expected)})`
          }`
        );
        if (ok) passed++;
      } catch (error) {
        console.error(`Error while testing input ${JSON.stringify(input)}: ${error.message}`);
      }
      total++;
    }

    console.log(`\n${passed}/${total} tests passed.`);
  }

  static compareValues(actual, expected) {
    if (typeof actual !== typeof expected) return false;
    if (Array.isArray(actual) && Array.isArray(expected)) {
      return JSON.stringify(actual) === JSON.stringify(expected);
    }
    return actual === expected;
  }
}

export default Helper;
