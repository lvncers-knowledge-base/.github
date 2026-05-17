# Knowledge Base 同期システム

対象Org:

* [lvncers-knowledge-base GitHub Organization](https://github.com/lvncers-knowledge-base)

目的:

* Org配下の全リポジトリをローカルに自動クローン
* 新規repo追加時に差分同期
* 将来的にObsidian Graph Viewで繋がりを可視化
* Markdownベースの知識ネットワークを構築

## 全体構成

```txt
GitHub Org
   ↓
sync script
   ↓
local vault/
   ├── repo-a/
   ├── repo-b/
   ├── repo-c/
   └── ...
   ↓
Obsidian Vault
   ↓
Graph View
```

各repoをそのままVault配下に置くことで、Obsidian側で横断検索・リンク解析・Graph表示ができる。

## おすすめディレクトリ構成

```sh
~/knowledge-vault/
├── repos/
│   ├── repo-a/
│   ├── repo-b/
│   └── repo-c/
├── scripts/
│   ├── sync_repos.py
│   └── generate_index.py
├── indexes/
│   └── repo_index.md
└── .obsidian/
```

repos/ 以下をObsidianで開くイメージ。

## Step 1: 全repoを自動クローンする

### 必要なもの

* git
* Python 3.10+
* python-dotenv
* GitHub Personal Access Token

GitHub Token:

* Settings
* Developer settings
* Personal access tokens
* Fine-grained token

### Fine-grained token 設定

```txt
Repository access:
  All repositories

Permissions:
  Metadata: Read-only
  Contents: Read-only
```

### 環境変数

scripts/ 配下に `.env` を置く。

```sh
GITHUB_TOKEN=ghp_xxxxx
```

.gitignore に `.env` を入れておくのがおすすめ。

```gitignore
.env
```

Python側では `python-dotenv` を使って読み込む。

### sync_repos.py

#### 実行方法

```bash
cd ~/knowledge-vault/scripts
pip install requests python-dotenv
python sync_repos.py
```

これで:

* 新repo → clone
* 既存repo → git pull

になる。
つまり「不足repo確認」と「同期」を同時にやってる。

## Step 2: 手動sync運用

「必要なタイミングで同期」がかなり扱いやすい。
例えば:

* 新repoを追加した後
* 作業開始前
* Obsidianを開く前
* 週1整理タイム

みたいな感じ。

### 実行コマンド

```bash
cd ~/knowledge-vault/scripts
python sync_repos.py
```

これだけで:

* 新repo → clone
* 既存repo → pull
* 削除repo以外を同期

してくれる。
つまり "今のOrg状態に合わせる" ボタンみたいな存在。

### おすすめ: shell alias化

.zshrc:

```bash
alias ksync='python ~/knowledge-vault/scripts/sync_repos.py'
```

すると `ksync` だけで同期できる。
かなり快適。

## Step 3: ObsidianでGraph表示する

重要なのは「repo同士のリンク」を作ること。
Graph Viewは:

```md
[[別ノート]]
```

を繋がりとして認識する。
だから:

* README
* index
* architecture
* notes

などで内部リンクを増やすと、巨大知識グラフになる。

### おすすめ運用

#### 各repoに index.md を置く

例:

```md
# AI Agents

## Related

- [[Vector Search]]
- [[RAG Pipeline]]
- [[Embedding System]]
```

これだけでGraphに線が出る。

## Step 4: 自動Index生成

repo同士の接続を増やしたいなら、
READMEやtagsを読んでindexを自動生成すると強い。

### generate_index.py

これで全repoをObsidian上で一覧化できる。

## 将来的にやると面白いもの

### 1. repo similarity graph

READMEをembedding化して:

* 類似repo
* 関連技術
* 近い概念

を自動リンク。
かなり知識ネットワーク感が出る。

### 2. 自動タグ付け

LLMで:

* #ai
* #infra
* #game
* #agent
* #rag

みたいにタグ生成。
Graphがかなり綺麗になる。

### 3. daily knowledge ingestion

今後:

* web clipping
* Claude/ChatGPT logs
* YouTube transcript
* research notes

もrepoとして入れると、第二脳感が強くなる。

### さらにおすすめ

## Obsidian Plugin

おすすめ:

* Dataview
* Excalidraw
* Juggl
* Breadcrumbs
* Omnisearch

特にJugglは知識グラフ探索がかなり強い。

### 理想系

最終的には:

```txt
GitHub = source of truth
Obsidian = knowledge UI
LLM = semantic layer
```

になる。
repoが増えるほど“脳”っぽくなっていく。
かなり面白い構成。
