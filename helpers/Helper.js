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

    for (const [input, expected] of Object.entries(testData)) {
      const result = solutionInstance.solution(input);
      const ok = result === expected;
      console.log(`"${input}" => ${ok ? 'PASSED' : `FAILED (got ${result})`}`);
      if (ok) passed++;
      total++;
    }

    console.log(`\n${passed}/${total} tests passed.`);
  }
}

export default Helper;
