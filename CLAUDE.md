# travel-agent-plugin

国内旅行の相談を手伝う Claude Code plugin です。相談役（concierge）がハブになり、調査役（access / scout / planner / inspector / reviewer）を呼び分けます。

## 旅行の相談を始めるとき

ユーザーが旅行の相談をしたい様子なら、次の入口から始めてください。

| 使う場所 | 始め方 |
|---|---|
| Claude Code のデスクトップアプリ（Code タブ）で、このリポジトリを開いたとき | `/travel-start`（最初の要望を続けて書いてもよい） |
| クラウドの Claude Code（claude.ai/code） | `/travel-start` |
| 手元の CLI | `claude --plugin-dir ./plugins/travel-agent --agent travel-agent:concierge` |
| plugin を入れた通常のセッション | `/travel-agent:start` |

- アプリとクラウドでは `--agent` を指定できません。`.claude/agents/` と `.claude/skills/` にあるコピーを使います。
- アプリとクラウドで保存される場所は、このリポジトリの `.travel-agent/trips/<旅行ID>/` です（git には入りません）。
- `/travel-start` で始めると、相談役はセッションのツールをすべて持ちます。それでも、自分で Web やコネクタを使わず、調査は調査役に任せます。

## 定義を直すとき

- 正は `plugins/travel-agent/` の側です。`.claude/` は生成物なので、直接は編集しません。
- 直したら `python3 scripts/sync_project_copy.py` で `.claude/` を作り直し、`--check` で一致を確かめます。
- 設計の方針は、次のとおりです。
  - 道具とやり方を渡して、あとはモデルに任せる。決まりを積み増さない。
  - 役割は分ける。ハブ（concierge）は、会話、呼び出し、受け渡し、保存、提示だけをする。
  - 利用者との会話は、短く聞いて短く答えられる形にする。長文を出さない。
- 段階ごとの流れは `docs/workflow.md`、決めた理由は `docs/design.md` にあります。
