from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = ROOT / "plugins" / "kero-seedance2"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "seedance-video-production"
SKILL_FILE = SKILL_ROOT / "SKILL.md"
AGENT_FILE = SKILL_ROOT / "agents" / "openai.yaml"
REFERENCES_ROOT = SKILL_ROOT / "references"
MARKETPLACE_FILE = ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_FILE = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
EVAL_FILE = ROOT / "evals" / "cases.json"

errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read_text(path: Path) -> str:
    if not path.is_file():
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> object:
    text = read_text(path)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {error}")
        return {}


def read_yaml(path: Path) -> object:
    text = read_text(path)
    if not text:
        return {}
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as error:
        errors.append(f"Invalid YAML in {path.relative_to(ROOT)}: {error}")
        return {}


required_files = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "requirements-dev.txt",
    MARKETPLACE_FILE,
    PLUGIN_FILE,
    SKILL_FILE,
    AGENT_FILE,
    EVAL_FILE,
]
for required_file in required_files:
    check(required_file.is_file(), f"Missing required file: {required_file.relative_to(ROOT)}")


# The installable plugin must not contain repository-only research or test assets.
plugin_top_level = {path.name for path in PLUGIN_ROOT.iterdir()} if PLUGIN_ROOT.is_dir() else set()
check(
    plugin_top_level == {".codex-plugin", "skills"},
    f"Plugin package contains unexpected top-level entries: {sorted(plugin_top_level)}",
)
skill_top_level = {path.name for path in SKILL_ROOT.iterdir()} if SKILL_ROOT.is_dir() else set()
check(
    skill_top_level == {"SKILL.md", "agents", "references"},
    f"Skill package contains unexpected top-level entries: {sorted(skill_top_level)}",
)


plugin = read_json(PLUGIN_FILE)
if isinstance(plugin, dict):
    check(plugin.get("name") == "kero-seedance2", "Plugin name must be kero-seedance2.")
    version = plugin.get("version")
    check(
        isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", version) is not None,
        "Plugin version must use strict semantic versioning.",
    )
    check(plugin.get("license") == "MIT", "Plugin manifest license must be MIT.")
    check(plugin.get("skills") == "./skills/", "Plugin manifest skills path must be ./skills/.")
    author = plugin.get("author")
    check(isinstance(author, dict) and bool(author.get("name")), "Plugin manifest needs author.name.")
    interface = plugin.get("interface")
    check(isinstance(interface, dict), "Plugin manifest needs an interface object.")
    if isinstance(interface, dict):
        for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            check(isinstance(interface.get(key), str) and bool(interface.get(key)), f"Plugin interface needs {key}.")
        prompts = interface.get("defaultPrompt")
        check(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "Plugin defaultPrompt must contain one to three prompts.")
        if isinstance(prompts, list):
            check(all(isinstance(prompt, str) and len(prompt) <= 128 for prompt in prompts), "Each plugin defaultPrompt must be a string of at most 128 characters.")


marketplace = read_json(MARKETPLACE_FILE)
if isinstance(marketplace, dict):
    check(marketplace.get("name") == "kero-seedance2-marketplace", "Unexpected marketplace name.")
    entries = marketplace.get("plugins")
    check(isinstance(entries, list) and len(entries) == 1, "Marketplace must contain exactly one plugin entry.")
    if isinstance(entries, list) and len(entries) == 1 and isinstance(entries[0], dict):
        entry = entries[0]
        check(entry.get("name") == "kero-seedance2", "Marketplace plugin name must match the manifest.")
        check(entry.get("source") == {"source": "local", "path": "./plugins/kero-seedance2"}, "Marketplace source must point to ./plugins/kero-seedance2.")
        check(entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "Marketplace policy is incomplete or invalid.")
        check(isinstance(entry.get("category"), str) and bool(entry.get("category")), "Marketplace plugin needs a category.")


skill_text = read_text(SKILL_FILE)
frontmatter_match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", skill_text)
check(frontmatter_match is not None, "SKILL.md must start with YAML frontmatter.")
if frontmatter_match:
    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as error:
        errors.append(f"Invalid SKILL.md frontmatter YAML: {error}")
        frontmatter = {}
    check(isinstance(frontmatter, dict) and set(frontmatter) == {"name", "description"}, "SKILL.md frontmatter must contain only name and description.")
    if isinstance(frontmatter, dict):
        check(frontmatter.get("name") == "seedance-video-production", "Skill name must be seedance-video-production.")
        description = frontmatter.get("description")
        check(isinstance(description, str) and 50 <= len(description) <= 500, "Skill description must be 50 to 500 characters.")

check(len(skill_text.splitlines()) <= 500, "SKILL.md must stay at or below 500 lines.")
check(re.search(r"\b(?:TODO|FIXME)\b", skill_text) is None, "SKILL.md contains TODO or FIXME.")
check("不要仅因用户提到镜头语言" in skill_text, "Skill trigger boundary must reject generic video-language triggers.")
check("特定训练模块" in skill_text, "Skill must distinguish semantic steering from an unverified internal mechanism.")


agent_text = read_text(AGENT_FILE)
agent = read_yaml(AGENT_FILE)
if isinstance(agent, dict):
    check(set(agent).issubset({"interface", "policy"}), "agents/openai.yaml contains unsupported top-level keys.")
    interface = agent.get("interface")
    policy = agent.get("policy")
    check(isinstance(interface, dict), "agents/openai.yaml needs interface metadata.")
    if isinstance(interface, dict):
        check(isinstance(interface.get("display_name"), str) and bool(interface.get("display_name")), "openai.yaml needs display_name.")
        short_description = interface.get("short_description")
        check(isinstance(short_description, str) and 25 <= len(short_description) <= 64, "openai.yaml short_description must be 25 to 64 characters.")
        default_prompt = interface.get("default_prompt")
        check(isinstance(default_prompt, str) and "$seedance-video-production" in default_prompt, "openai.yaml default_prompt must mention $seedance-video-production.")
    check(isinstance(policy, dict) and policy.get("allow_implicit_invocation") is True, "Implicit invocation must remain enabled with a narrow trigger description.")

for line_number, line in enumerate(agent_text.splitlines(), start=1):
    match = re.match(r"^\s+[a-z_]+:\s+(.+)$", line)
    if match and match.group(1) not in {"true", "false"}:
        value = match.group(1)
        check(value.startswith('"') and value.endswith('"'), f"openai.yaml string on line {line_number} must be quoted.")


reference_files = sorted(REFERENCES_ROOT.glob("*.md")) if REFERENCES_ROOT.is_dir() else []
linked_references = set(re.findall(r"references/([^)]+\.md)", skill_text))
all_references = {path.name for path in reference_files}
check(linked_references == all_references, f"Every reference must be linked directly from SKILL.md. Missing={sorted(all_references - linked_references)} extra={sorted(linked_references - all_references)}")

runtime_reference_text = "\n".join(read_text(path) for path in reference_files)
check("3–10 秒" not in runtime_reference_text and "3-10 秒" not in runtime_reference_text, "Runtime references must not prescribe a fixed 3-10 second reference clip.")
check("会把生成引向模型训练" not in skill_text + runtime_reference_text, "Runtime Skill must not claim an unverified training mechanism.")


markdown_files = [ROOT / "README.md", ROOT / "docs" / "sources-and-maintenance.md", ROOT / "research" / "feishu-content-integration.md", SKILL_FILE, *reference_files]
link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for markdown_file in markdown_files:
    content = read_text(markdown_file)
    for raw_target in link_pattern.findall(content):
        target = unquote(raw_target.strip().split("#", 1)[0])
        if not target or re.match(r"^(?:https?:|mailto:)", target):
            continue
        resolved = (markdown_file.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"{markdown_file.relative_to(ROOT)} links outside the repository: {raw_target}")
            continue
        check(resolved.exists(), f"{markdown_file.relative_to(ROOT)} has a broken link: {raw_target}")


cases = read_json(EVAL_FILE)
if isinstance(cases, list):
    check(len(cases) >= 18, "evals/cases.json must contain at least 18 cases.")
    ids: set[str] = set()
    negative_trigger_count = 0
    for index, case in enumerate(cases, start=1):
        check(isinstance(case, dict), f"Eval case {index} must be an object.")
        if not isinstance(case, dict):
            continue
        case_id = case.get("id")
        check(isinstance(case_id, str) and bool(case_id), f"Eval case {index} needs an id.")
        if isinstance(case_id, str):
            check(case_id not in ids, f"Duplicate eval id: {case_id}")
            ids.add(case_id)
        check(isinstance(case.get("request"), str) and bool(case.get("request")), f"Eval case {case_id} needs a request.")
        check(isinstance(case.get("expect"), list) and bool(case.get("expect")), f"Eval case {case_id} needs expectations.")
        check(isinstance(case.get("avoid"), list) and bool(case.get("avoid")), f"Eval case {case_id} needs avoid rules.")
        if "should_trigger" in case:
            check(isinstance(case["should_trigger"], bool), f"Eval case {case_id} should_trigger must be boolean.")
            if case["should_trigger"] is False:
                negative_trigger_count += 1
    check(negative_trigger_count >= 1, "At least one eval must test a negative trigger boundary.")
else:
    errors.append("evals/cases.json must contain a JSON array.")


if errors:
    print("Repository validation failed:\n", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Repository validation passed.")
