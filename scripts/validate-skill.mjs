import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];

function read(relativePath) {
  const absolutePath = path.join(root, relativePath);
  if (!fs.existsSync(absolutePath)) {
    errors.push(`Missing required file: ${relativePath}`);
    return "";
  }
  return fs.readFileSync(absolutePath, "utf8");
}

function assert(condition, message) {
  if (!condition) errors.push(message);
}

const skill = read("SKILL.md");
const agent = read(path.join("agents", "openai.yaml"));
const evalText = read(path.join("evals", "cases.json"));

const frontmatterMatch = skill.match(/^---\r?\n([\s\S]*?)\r?\n---/);
assert(frontmatterMatch, "SKILL.md must start with YAML frontmatter.");

if (frontmatterMatch) {
  const keys = [...frontmatterMatch[1].matchAll(/^([a-zA-Z0-9_-]+):/gm)].map((match) => match[1]);
  assert(keys.length === 2 && keys.includes("name") && keys.includes("description"), "Frontmatter must contain only name and description.");
  assert(/^name:\s*seedance-video-production\s*$/m.test(frontmatterMatch[1]), "Skill name must be seedance-video-production.");
}

assert(skill.split(/\r?\n/).length <= 500, "SKILL.md must stay at or below 500 lines.");
assert(!/\b(TODO|FIXME)\b/.test(skill), "SKILL.md contains an unfinished TODO or FIXME.");
assert(agent.includes("$seedance-video-production"), "agents/openai.yaml default_prompt must mention $seedance-video-production.");
assert(/allow_implicit_invocation:\s*true/.test(agent), "Implicit invocation must remain enabled.");

const markdownFiles = [
  "SKILL.md",
  "README.md",
  ...fs.readdirSync(path.join(root, "references"))
    .filter((fileName) => fileName.endsWith(".md"))
    .map((fileName) => path.join("references", fileName)),
  ...(fs.existsSync(path.join(root, "research"))
    ? fs.readdirSync(path.join(root, "research"))
        .filter((fileName) => fileName.endsWith(".md"))
        .map((fileName) => path.join("research", fileName))
    : []),
];

for (const markdownFile of markdownFiles) {
  const content = read(markdownFile);
  const linkPattern = /\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)/g;
  for (const match of content.matchAll(linkPattern)) {
    const target = decodeURIComponent(match[1].split("#")[0]);
    if (/^(?:https?:)?\/\//.test(target)) continue;
    const resolved = path.resolve(path.dirname(path.join(root, markdownFile)), target);
    assert(fs.existsSync(resolved), `${markdownFile} has a broken link: ${match[1]}`);
  }
}

try {
  const cases = JSON.parse(evalText);
  assert(Array.isArray(cases) && cases.length >= 5, "evals/cases.json must contain at least five cases.");
  const ids = new Set();
  for (const [index, testCase] of cases.entries()) {
    assert(typeof testCase.id === "string" && testCase.id.length > 0, `Eval case ${index + 1} needs an id.`);
    assert(!ids.has(testCase.id), `Duplicate eval id: ${testCase.id}`);
    ids.add(testCase.id);
    assert(typeof testCase.request === "string" && testCase.request.length > 0, `Eval case ${testCase.id} needs a request.`);
    assert(Array.isArray(testCase.expect) && testCase.expect.length > 0, `Eval case ${testCase.id} needs expectations.`);
    assert(Array.isArray(testCase.avoid) && testCase.avoid.length > 0, `Eval case ${testCase.id} needs avoid rules.`);
  }
} catch (error) {
  errors.push(`evals/cases.json is invalid JSON: ${error.message}`);
}

if (errors.length > 0) {
  console.error("Skill validation failed:\n");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log("Skill validation passed.");
