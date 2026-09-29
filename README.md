# DeckArt

メーカーの説明資料に使えるPNGイラスト・背景と、SVGアイコン・図解・グラフ・説明パーツ。生成AIが用途を検索し、GitHubから元の画像を取得できます。

**[素材一覧](https://sakurai-yoshi.github.io/deckart/)** · **[一式ZIP](https://github.com/sakurai-yoshi/deckart/releases/download/v1.0.0/deckart.zip)** · **[AI向け入口](llms.txt)** · **[用途索引](catalog.json)**

## 生成AIに渡す

```text
https://raw.githubusercontent.com/sakurai-yoshi/deckart/v1.0.0/llms.txt
```

`catalog.json` で用途・形式・透過・編集の可否を確認して選びます。`metadata_path` で描写の意味と配置条件、`path` で元ファイルを取得します。拡張子は `format` に合わせ、`sha256` を照合します。RAG用の [catalog.ndjson](catalog.ndjson) は1素材1行です。同じタグまたはコミットの索引と画像を使ってください。

| 素材 | 形式 | 使い方 |
|---|---|---|
| イラスト | 透過PNG | 人物の行為や物同士の関係。資料の余白に配置 |
| 背景 | 不透明PNG | 16:9全体に配置し、指定領域に文章や図表を追加 |
| アイコン・図解・グラフ・説明パーツ | SVG | 拡大・配色変更。対応素材は文字・実データの入力も可能 |

## 検索・書き出し

Python 3.10以上。追加パッケージは不要です。

検索語は空白区切りでAND検索します。「確認」「品質 改善」など、短い用途語から探してください。

```sh
python3 scripts/library.py search '説明' --format png
python3 scripts/library.py search '承認 差戻し' --themeable
python3 scripts/library.py show illustration/explaining
python3 scripts/library.py export illustration/explaining --output ./exports/explaining.png
python3 scripts/library.py export background/cover-prismatic-depth --output ./exports/cover.png
python3 scripts/library.py export icon/person --accent '#005BAC' --output ./exports/person.svg
python3 scripts/library.py export --request examples/progress-data.json --output ./exports/progress.svg
```

画像とJSONを保存し、成功時は `file`・`format`・ハッシュなどをJSONで返します。`--stdout` は画像のバイト列のみを返します。[入力仕様](request.schema.json)

PNGは元の画素と透過を保ってコピーします。配色・文字・数値の変更、別形式への変換は受け付けません。SVGは基本の青・ブランド色・モノクロに対応し、注意・増減の色を分離しています。[配色仕様](themes.json)

## 資料へ配置する

PowerPointの［挿入］→［画像］で配置し、縦横比を固定します。PNGの `width`・`height` は実画素数です。イラストの `placement` は構図・向き・人数・推奨配置幅を示します。

背景の `content_areas` は、`canvas` の論理座標を基準にした文章・図表の配置領域です。PNGの画素数と混同せず、スライドへ同じ比率で変換します。文字はPowerPoint側で追加してください。SVGの `labels` には文字の位置と長さの目安があります。

グラフの配布SVGは作例です。実データは `data_input` の仕様に従って書き出すと、図形と数値を同時に更新できます。

一式ZIPを展開した `index.html` はオフラインでも閲覧・個別保存できます。PNGを含む選択ZIPを作る際は、画面の案内に従って展開先の `media` フォルダを選びます。[利用ガイド](web/guide.html)

## 更新・ライセンス

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests
python3 scripts/check_public.py --history
```

SVGの定義は `scripts/sets/`、生成PNGは `media/`、用途と生成指示は `sources/`、軽量プレビューは `previews/` に置きます。変更時は索引・個別メタデータ・ZIPも再生成します。`deckart.zip` はビルドで生成し、GitHub Releaseへ添付します。

公開用Gitメールを使い、`git config core.hooksPath scripts/hooks` で公開情報の検査を有効にできます。CIはGitHubが生成するPR検証用マージコミットも含めて検査します。

素材・プレビュー・メタデータは [CC0 1.0](LICENSE-ASSETS)。商用利用・改変・再配布・クレジット不要。生成・閲覧コードは [MIT](LICENSE)です。
