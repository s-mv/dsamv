// this is your input
const stdin = await new Promise((resolve) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", chunk => data += chunk);
  process.stdin.on("end", () => resolve(data));
});

// you can split multiline input by using stind.split("\n")
// this code is equivalent to arrays/js/IsUnique.js
const line = stdin;
const seen = new Set();

for (let char of line) {
  if (seen.has(char)) {
    // console.log output to be read by the tests
    console.log("false");
    process.exit(0);
  }
  seen.add(char);
}

// console.log output to be read by the tests
console.log("true");
