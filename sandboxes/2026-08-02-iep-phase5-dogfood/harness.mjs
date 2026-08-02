const input = await new Promise((resolve, reject) => {
  let value = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => {
    value += chunk;
  });
  process.stdin.on("end", () => resolve(value));
  process.stdin.on("error", reject);
});

const request = JSON.parse(input);
const question = request.task.input.question;

process.stdout.write(
  JSON.stringify({
    answer: "4",
    question,
    rationale: "2 + 2 = 4",
  }),
);
