const stdin = await new Promise((resolve) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", chunk => data += chunk);
  process.stdin.on("end", () => resolve(data));
});


const line = stdin;
const seen = new Set();

for (let char of line) {
  if (seen.has(char)) {
    console.log("false");
    process.exit(0);
  }
  seen.add(char);
}

console.log("true");
