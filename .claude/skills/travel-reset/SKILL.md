---
name: travel-reset
description: travel-agent が保存した旅行のデータ（条件、候補、調べた結果）を一覧し、選んだものを消す。
disable-model-invocation: true
argument-hint: "[旅行ID | all（省略すると一覧を表示）]"
---

<!-- このファイルは scripts/sync_project_copy.py が plugins/travel-agent/skills/reset/SKILL.md から作った生成物です。直接編集せず、元のファイルを直してからスクリプトを実行してください。 -->

travel-agent が保存したデータを消します。会話は日本語です。

データフォルダ：`.travel-agent`
旅行ごとのデータ：`.travel-agent/trips/<旅行ID>/`

指定：$ARGUMENTS

## 手順

1. `.travel-agent/trips/` の下にあるフォルダを一覧します。何もなければ「保存されたデータはありません」と伝えて終わります。
2. それぞれのフォルダについて、旅行 ID と、`conditions.json` があればその日程とエリアを、1行ずつ見せます。
3. 指定がなければ、どれを消すかを聞きます（1件、複数、全部、やめる）。
4. 指定が旅行 ID なら、その1件だけが対象です。`all` なら全部が対象です。
5. **消す前に、対象のフォルダのパスを見せて、確認を取ります。** 確認が取れてから消します。
6. 消すのは `.travel-agent/trips/` の下のフォルダだけです。それより上のフォルダや、ほかの場所のファイルは消しません。パスに `..` が含まれる指定は受け付けません。
7. 消したら、何を消したかを伝えます。

ファイルを消すツールが使えない場合は、消さずに、ユーザーが自分で消すためのコマンドを伝えます。

```
rm -rf ".travel-agent/trips/<旅行ID>"
```

## 補足

- このスキルが消すのは、travel-agent が保存したデータだけです。Claude Code 本体が保存している会話の記録は、別に残ります。
- データフォルダは、リポジトリの中の `.travel-agent/` です（`.gitignore` に入っています）。クラウド上の Claude Code では、環境が作り直されると消えます。
