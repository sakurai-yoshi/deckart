# DeckArt

メーカーの説明資料に使えるPNGイラスト・背景と、SVGアイコン・図解・グラフ・説明パーツ。生成AIが用途から選び、GitHubから元の画像を取得できます。

**[素材一覧](https://sakurai-yoshi.github.io/deckart/)** · **[一式ZIP](https://github.com/sakurai-yoshi/deckart/releases/download/v2.1.0/deckart.zip)** · **[AI向け入口](llms.txt)** · **[全素材の見出し](catalog.txt)** · **[用途別索引](categories.json)**

## 生成AIに渡す

```text
https://raw.githubusercontent.com/sakurai-yoshi/deckart/main/llms.txt
```

[用途別索引](categories.json) から、経営・計画・品質・生産・調達・開発・安全・環境・人材・顧客・会計・情報・説明・背景の候補を取得できます。一つの用途で複数種類を見比べられます。汎用のグラフ・説明関係は [説明・伝達](catalogs/communication.json)、背景は [背景・装飾](catalogs/backgrounds.json) から、どの業務にも組み合わせられます。[catalog.txt](catalog.txt) は全素材の見出し、[catalog.json](catalog.json) は一括処理用の全索引です。候補の `preview_path` を開き、伝えたい内容に合う素材を選びます。`preview_has_example_labels: true` のプレビューは作例文字を含むSVGで、内容が合う場合はそのまま使えます。用途・意味・キーワードは使用例です。記載された場面以外にも使えます。

`metadata_path` に詳しい描写、`path` に元画像があります。同じタグまたはコミットの索引・メタデータ・画像を使い、元画像は `sha256`、文字入りSVGは `preview_sha256` を照合してください。RAG用の [catalog.ndjson](catalog.ndjson) は1素材1行です。

| 素材 | 形式 | 活用例 |
|---|---|---|
| イラスト | 透過PNG | 行為や物同士の関係を伝える、主題を印象づける |
| 背景 | 不透明PNG | 全面・部分・トリミングで資料に質感と視線の流れを添える |
| アイコン | SVG | 項目・対象・行為を見分けやすくする |
| 図解・説明パーツ | SVG | 流れ・比較・関係・条件を可視化する |
| グラフ | SVG | 実データの形と数値を一緒に表す |

## 検索・書き出し

Python 3.10以上。追加パッケージは不要です。

用途を日本語・英語で検索できます。用途分類・種類・形式・配色変更などのフィルターは必要なときに指定します。既定の検索は全分類を横断します。既定は20件。`--offset` で続き、`--limit 0` で全候補を取得できます。

```sh
python3 scripts/library.py search '品質改善の流れを説明する'
python3 scripts/library.py search 'quality improvement' --offset 20
python3 scripts/library.py search '' --limit 0
python3 scripts/library.py show illustration/explaining
python3 scripts/library.py export illustration/explaining --output ./exports/explaining.png
python3 scripts/library.py export background/cover-prismatic-depth --output ./exports/cover.png
python3 scripts/library.py export icon/person --accent '#005BAC' --output ./exports/person.svg
python3 scripts/library.py export process/approval-return --example-labels --output ./exports/approval-preview.svg
python3 scripts/library.py export --request examples/progress-data.json --output ./exports/progress.svg
```

検索は `total`・`returned`・`next_offset`・`filters` と候補をJSONで返します。書き出しは画像とJSONを保存し、形式とハッシュを返します。`--stdout` は画像のバイト列を返します。[入力仕様](request.schema.json)

この書き出しツールではPNGを元の画素・透過のままコピーします。SVGは基本の青・任意のブランド色・モノクロに対応し、文字・実データを入力できる素材もあります。[配色仕様](themes.json)

## 資料へ配置する

PowerPointの［挿入］→［画像］で配置します。拡大縮小は縦横比を保ち、位置・大きさ・トリミングは実際の文章や図表に合わせて決めます。背景の上に白い面を重ねるなどして読みやすさを調整できます。完成したスライドを表示し、文字の収まり・コントラスト・意図しない重なり・切れを確認してください。

`width`・`height` と `canvas` は画像自体の寸法です。イラストの `composition` は構図・向き・人数の説明です。いずれも配置の指定ではありません。SVGの図解・説明パーツ・グラフは、選定用プレビューに作例の文字を表示します。作例の内容が合えば `preview_path` の文字入りSVGを直接使えます。自分で文章を配置する場合は `path` の図形のみSVGを選び、PowerPointで文字を追加できます。画像内の文字変更には `labels` を使います。`--example-labels` では文字入りのSVGも書き出せます。グラフの配布SVGは作例。実データは `data_input` に従って書き出せます。

素材はCC0です。お使いのソフトウェアでトリミング・改変・配色変更もできます。ツールが対応する書き出し機能と、素材の利用条件は別です。

素材一覧の個別保存は［プレビューの作例文字］に連動します。表示中なら文字入りSVG、非表示なら図形のみSVGを保存します。拡大画面では両方から選べます。選択・全素材のまとめて保存は、文字のある素材ごとに同じ配色の図形のみSVGと文字入りSVGを両方収録し、`catalog.json` と `metadata/` にそれぞれのパスとハッシュを記録します。

一式ZIPの `index.html` はオフラインでも閲覧・個別保存できます。PNGを含む選択ZIPを作る際は、画面の案内に従って展開先の `media` フォルダを選びます。[利用ガイド](web/guide.html)

## 更新・ライセンス

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests
python3 scripts/check_public.py --history
```

SVGの定義は `scripts/sets/`、生成PNGは `media/`、用途と生成指示は `sources/`、軽量プレビューは `previews/` に置きます。主たる用途分類は `scripts/categories.py` に集約します。変更時は索引・個別メタデータ・ZIPも再生成します。`deckart.zip` はGitHub Releaseへ添付します。

公開用Gitメールを使い、`git config core.hooksPath scripts/hooks` で公開情報の検査を有効にできます。CIはGitHubが生成するPR検証用マージコミットも含めて検査します。

素材・プレビュー・メタデータは [CC0 1.0](LICENSE-ASSETS)。商用利用・改変・再配布・クレジット不要。生成・閲覧コードは [MIT](LICENSE)です。
