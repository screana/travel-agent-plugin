#!/usr/bin/env python3
"""plugin の定義から、プロジェクト用のコピー（.claude/ の下）を作る。

クラウド上の Claude Code は plugin を読み込まないので、このリポジトリを
そのまま開いたときに使えるよう、同じ定義を .claude/agents/ と
.claude/skills/ にも置いている。正は plugins/travel-agent/ の側で、
.claude/ の下は、このスクリプトが作る生成物。直接は編集しない。

使い方（リポジトリのルートで）:
    python3 scripts/sync_project_copy.py           # コピーを作り直す
    python3 scripts/sync_project_copy.py --check   # ずれていないかを確かめる（ずれていれば終了コード 1）

行うのは、ファイルのコピーと、下の REPLACEMENTS にある決まった文字列の
置き換えだけ。ネットワークには触れない。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "plugins" / "travel-agent"
DST = ROOT / ".claude"

# 元のファイル -> 生成先（どちらもリポジトリのルートからの相対パス）
FILES = {
    "plugins/travel-agent/agents/concierge.md": ".claude/agents/concierge.md",
    "plugins/travel-agent/agents/scout.md": ".claude/agents/scout.md",
    "plugins/travel-agent/agents/inspector.md": ".claude/agents/inspector.md",
    "plugins/travel-agent/agents/access.md": ".claude/agents/access.md",
    "plugins/travel-agent/skills/start/SKILL.md": ".claude/skills/travel-start/SKILL.md",
    "plugins/travel-agent/skills/reset/SKILL.md": ".claude/skills/travel-reset/SKILL.md",
    "plugins/travel-agent/skills/report/SKILL.md": ".claude/skills/travel-report/SKILL.md",
}

# 決まった文字列の置き換え。上から順に、すべてのファイルに当てる。
REPLACEMENTS = [
    # plugin では展開される変数。プロジェクト用では展開されないので、実際の場所に置き換える
    ("${CLAUDE_PLUGIN_ROOT}/agents/", ".claude/agents/"),
    ("${CLAUDE_PLUGIN_ROOT}/skills/report/", ".claude/skills/travel-report/"),
    ("${CLAUDE_PLUGIN_DATA}", ".travel-agent"),
    # スキルの呼び名
    ("/travel-agent:start", "/travel-start"),
    ("/travel-agent:reset", "/travel-reset"),
    ("/travel-agent:report", "/travel-report"),
    ("\nname: start\n", "\nname: travel-start\n"),
    ("\nname: reset\n", "\nname: travel-reset\n"),
    ("\nname: report\n", "\nname: travel-report\n"),
    # エージェントの呼び名（plugin では「travel-agent:名前」、プロジェクト用では名前だけ）
    ("travel-agent:concierge", "concierge"),
    ("travel-agent:scout", "scout"),
    ("travel-agent:inspector", "inspector"),
    ("travel-agent:access", "access"),
    # データが消える条件の説明
    (
        "- plugin をアンインストールすると、データフォルダごと消えます。",
        "- データフォルダは、リポジトリの中の `.travel-agent/` です（`.gitignore` に入っています）。クラウド上の Claude Code では、環境が作り直されると消えます。",
    ),
]

# 置き換えのあとに残っていてはいけない文字列
FORBIDDEN = ["${CLAUDE_PLUGIN_", "travel-agent:"]

NOTICE = (
    "<!-- このファイルは scripts/sync_project_copy.py が {src} から作った生成物です。"
    "直接編集せず、元のファイルを直してからスクリプトを実行してください。 -->\n"
)


def render(src_rel: str) -> str:
    text = (ROOT / src_rel).read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    for bad in FORBIDDEN:
        if bad in text:
            raise SystemExit(f"置き換えのあとに「{bad}」が残っています: {src_rel}")
    # frontmatter（先頭の --- から次の --- まで）の直後に、生成物である旨を入れる
    if not text.startswith("---\n"):
        raise SystemExit(f"frontmatter がありません: {src_rel}")
    end = text.index("\n---\n", 4) + len("\n---\n")
    return text[:end] + "\n" + NOTICE.format(src=src_rel) + text[end:]


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for src_rel, dst_rel in FILES.items():
        want = render(src_rel)
        dst = ROOT / dst_rel
        have = dst.read_text(encoding="utf-8") if dst.exists() else None
        if have == want:
            continue
        if check:
            stale.append(dst_rel)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(want, encoding="utf-8")
            print(f"書き出しました: {dst_rel}")
    if check:
        if stale:
            print("プロジェクト用のコピーが、plugin の定義とずれています:")
            for p in stale:
                print(f"  {p}")
            print("python3 scripts/sync_project_copy.py を実行して、作り直してください。")
            return 1
        print("プロジェクト用のコピーは、plugin の定義と一致しています。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
