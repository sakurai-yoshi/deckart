'use strict';
const library=JSON.parse(document.getElementById('library').textContent);
const settings=JSON.parse(document.getElementById('settings').textContent);
const searchIndex=DeckArtSearch.prepare(library,settings.search);
const $=id=>document.getElementById(id),svgNS='http://www.w3.org/2000/svg';
const kindNames={diagram:'図解',illustration:'イラスト',icon:'アイコン',chart:'数値・グラフ',background:'背景',part:'説明パーツ'};
const cache=new Map(),baseSvg=new Map(),localMedia=new Map();
let mode='blue',theme=resolveTheme(),kind='',active=null,opener=null,noticeTimer;
let selected=new Set();
try{selected=new Set(JSON.parse(localStorage.getItem('deckart:selected')||'[]').filter(id=>library.some(a=>a.id===id)));}catch{}
function element(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
function blobURL(blob){return URL.createObjectURL(blob);}
function notify(text){$('notice').textContent=text;clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>{$('notice').textContent='';},4500);}
function svgFor(a,resolved=theme){if(!baseSvg.has(a.id))baseSvg.set(a.id,new TextDecoder().decode(Uint8Array.from(atob(a.download),c=>c.charCodeAt(0))));return themeSVG(baseSvg.get(a.id),resolved);}
function artURL(a,full=false){if(a.format==='png')return full?a.path:(a.preview_path||a.path);const key=JSON.stringify(theme)+':'+a.id;if(!cache.has(key))cache.set(key,blobURL(new Blob([svgFor(a)],{type:'image/svg+xml'})));return cache.get(key);}
function themeName(){return mode==='mono'?'モノクロ':mode==='blue'?'基本の青':'ブランド色';}
function fileName(a,selectedMode=mode,resolved=theme){if(a.format==='png')return a.id.replace('/','--')+'.png';return a.id.replace('/','--')+'--'+(selectedMode==='brand'?resolved.colors.accent.slice(1).toLowerCase():selectedMode)+'.svg';}
function makeArt(a,full=false){
 const art=element('div','art '+a.kind),canvas=element('div','canvas'),img=element('img');
 img.src=artURL(a,full);img.alt=a.title;img.width=a.width;img.height=a.height;img.loading='lazy';img.dataset.id=a.id;canvas.append(img);
 const overlay=document.createElementNS(svgNS,'svg');overlay.setAttribute('class','labels');overlay.setAttribute('viewBox',`0 0 ${a.width} ${a.height}`);overlay.setAttribute('aria-hidden','true');
 for(const l of a.labels){const text=document.createElementNS(svgNS,'text'),x=l.align==='left'?l.x:l.x+l.width/2,lines=l.text.split('\n'),font=l.font_size;
  text.setAttribute('text-anchor',l.align==='left'?'start':'middle');text.setAttribute('font-size',font);text.setAttribute('font-weight','500');text.setAttribute('fill',theme.colors[l.color_role]);text.dataset.role=l.color_role;
  lines.forEach((value,i)=>{const span=document.createElementNS(svgNS,'tspan');span.setAttribute('x',x);span.setAttribute('y',l.y+l.height/2+(i-(lines.length-1)/2)*font*1.4+font*.35);span.textContent=value;text.append(span);});overlay.append(text);
 }
 canvas.append(overlay);art.append(canvas);return art;
}
function downloadLink(a,cls,text){const link=element('a',cls,text);link.href=artURL(a,true);link.download=fileName(a);link.dataset.asset=a.id;link.setAttribute('aria-label',a.title+'の'+a.format.toUpperCase()+'を保存');return link;}
function setHash(){const p=new URLSearchParams();if($('search').value)p.set('q',$('search').value);if($('category').value)p.set('category',$('category').value);if(kind)p.set('kind',kind);if($('format').value)p.set('format',$('format').value);if($('transparent').checked)p.set('transparent','1');if($('themeable').checked)p.set('themeable','1');if(mode!=='blue')p.set('theme',mode);if(mode==='brand')p.set('accent',theme.requested_accent);if(!$('examples').checked)p.set('labels','0');if($('selected-only').checked)p.set('selected','1');if(active)p.set('asset',active);try{history.replaceState(null,'','#'+p);}catch{}}
function updateSelection(){
 try{localStorage.setItem('deckart:selected',JSON.stringify([...selected]));}catch{}
 document.querySelectorAll('input[data-select]').forEach(e=>{e.checked=selected.has(e.dataset.select);});
 $('selection-bar').hidden=!selected.size;$('selected-count').textContent=`${selected.size}点を選択中`;
 if(active){const on=selected.has(active);$('detail-select').textContent=on?'選択から外す':'まとめて保存に追加';$('detail-select').setAttribute('aria-pressed',String(on));}
}
function toggleSelected(id){if(selected.has(id))selected.delete(id);else selected.add(id);updateSelection();filter();}
const display=DeckArtSearch.rank(searchIndex,'').assets;
const cards=display.map(a=>{
 const card=element('article');card.dataset.id=a.id;
 const imageButton=element('button','art-button');imageButton.type='button';imageButton.setAttribute('aria-label',a.title+'を拡大');imageButton.append(makeArt(a));imageButton.addEventListener('click',()=>{opener=imageButton;openDetail(a);});
 const select=element('label','choose'),checkbox=element('input');checkbox.type='checkbox';checkbox.dataset.select=a.id;checkbox.setAttribute('aria-label',a.title+'をまとめて保存に追加');checkbox.addEventListener('change',()=>toggleSelected(a.id));select.append(checkbox,element('span','','選ぶ'));
 const bottom=element('div','card-bottom'),title=element('div');title.append(element('h2','',a.title),element('p','',a.data?'数値は作例':a.category.slice(3)));bottom.append(title,downloadLink(a,'save',a.format.toUpperCase()+'保存'));
 card.append(imageButton,select,bottom);$('grid').append(card);return card;
});
const cardById=new Map(cards.map(card=>[card.dataset.id,card]));
for(const value of [...new Set(library.map(a=>a.category))]){const o=element('option','',value.slice(3));o.value=value;$('category').append(o);}
for(const [value,label] of [['','すべて'],...Object.entries(kindNames)]){const b=element('button','',label);b.type='button';b.dataset.kind=value;b.setAttribute('aria-pressed',String(!value));b.addEventListener('click',()=>{kind=value;filter();});$('types').append(b);}
function setTheme(value,save=true){
 const next=['blue','brand','mono'].includes(value)?value:'blue';let resolved;
 try{resolved=resolveTheme(next==='brand'?$('accent').value:'#2864F0',next==='mono');$('accent').setCustomValidity('');}
 catch(error){$('accent').setCustomValidity(error.message);$('accent').reportValidity();return false;}
 mode=next;theme=resolved;$('detail-palette').value=mode;$('brand-control').hidden=mode!=='brand';
 document.querySelectorAll('#palettes input').forEach(e=>{e.checked=e.value===mode;});
 $('theme-note').textContent=theme.adjustments.length?`白い記号を読めるよう、強調色を ${theme.colors.accent} に調整しています。`:mode==='brand'?'輪郭と注意・増減の色を保ち、強調箇所へブランド色を使います。':mode==='mono'?'色に頼らず、形・位置・符号で関係を読み取れます。':'';
 document.querySelectorAll('img[data-id]').forEach(e=>{e.src=artURL(library.find(a=>a.id===e.dataset.id),Boolean(e.closest('#detail-art')));});
 document.querySelectorAll('a[data-asset]').forEach(e=>{const a=library.find(a=>a.id===e.dataset.asset);e.href=artURL(a,true);e.download=fileName(a);});
 document.querySelectorAll('text[data-role]').forEach(e=>e.setAttribute('fill',theme.colors[e.dataset.role]));
 if(save)setHash();return true;
}
function filter(save=true){
 const focused=document.activeElement,focusedCard=focused?.closest('#grid article');
 const filters={};if(kind)filters.kind=kind;if($('category').value)filters.category=$('category').value;if($('format').value)filters.format=$('format').value;if($('transparent').checked)filters.transparent=true;if($('themeable').checked)filters.themeable=true;
 const results=DeckArtSearch.rank(searchIndex,$('search').value,filters).assets.filter(a=>!$('selected-only').checked||selected.has(a.id)),fragment=document.createDocumentFragment();
 cards.forEach(card=>{card.hidden=true;});
 for(const a of results){const card=cardById.get(a.id);card.hidden=false;fragment.append(card);}$('grid').append(fragment);
 if(focusedCard&&!focusedCard.hidden)focused.focus({preventScroll:true});
 $('count').value=`${$('search').value.trim()?'関連する ':''}${results.length} / ${library.length} 点`;$('empty').hidden=results.length>0;document.body.classList.toggle('with-labels',$('examples').checked);
 document.querySelectorAll('#types button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind===kind)));
 if(save)setHash();
}
function openDetail(a,save=true){
 active=a.id;$('detail-title').textContent=a.title;$('detail-art').replaceChildren(makeArt(a,true));$('detail-art').querySelector('img').loading='eager';
 $('detail-ratio').textContent=`${a.format.toUpperCase()} · ${a.width} × ${a.height}${a.format==='png'?' px':''}`;$('use-case').textContent=a.guidance.use_case;$('message').textContent=a.guidance.message;
 $('reading').replaceChildren(...a.guidance.reading.map(t=>element('li','',t)));
 $('detail-save').replaceChildren(downloadLink(a,'primary download',a.format==='png'?'PNGを保存':'この配色でSVGを保存'));
 $('detail-palette').closest('.detail-palette').hidden=!a.render.theme;$('format-note').textContent=a.format==='png'?(a.transparent?'背景透過のPNG。スライド上の任意の位置に配置できます。':'不透明のPNG。全体の背景や一部の装飾として使えます。文章・図表の位置は資料に合わせて調整できます。'):'SVG図形。配色の変更と拡大に対応しています。';$('label-note').hidden=!a.labels.length;$('label-explanation').hidden=!a.labels.length;$('detail-labels').checked=$('examples').checked;$('detail-palette').value=mode;
 $('asset-id').textContent=a.id;if(a.composition){const framing={'waist-up':'上半身','full-body':'全身',object:'物・道具'},facing={left:'左向き',right:'右向き',front:'正面',inward:'向かい合う',down:'下向き'},facts=[framing[a.composition.framing],facing[a.composition.facing]];if(a.composition.people_count)facts.push(`人物${a.composition.people_count}人`);$('format-note').textContent+=` 描写：${facts.filter(Boolean).join('・')}。`;}$('filename').textContent=a.path;$('keywords').textContent=a.keywords.join(' / ');$('slots').replaceChildren(...a.labels.map(l=>element('li','',`${l.id} / ${l.role}：${l.text.replaceAll('\n',' ')}`)));
 $('data-note').hidden=!a.data;$('data-detail').hidden=!a.data;$('data-values').replaceChildren();
 if(a.data){const table=element('table'),head=element('tr');head.append(element('th','','系列'),element('th','','値'));const thead=element('thead');thead.append(head);table.append(thead);const tbody=element('tbody');for(const s of a.data.series){const row=element('tr');row.append(element('th','',s.label),element('td','',s.values.join(' / ')));tbody.append(row);}table.append(tbody);$('data-values').append(element('p','',a.data.categories.join(' / ')),table,element('p','',`単位：${a.data.unit}`));}
 document.querySelectorAll('#detail details').forEach(d=>d.open=false);updateSelection();if(!$('detail').open)$('detail').showModal();$('detail').scrollTop=0;if(save)setHash();
}
function restore(){
 const p=new URLSearchParams(location.hash.slice(1));$('search').value=p.get('q')||'';kind=kindNames[p.get('kind')]?p.get('kind'):'';
 $('category').value=library.some(a=>a.category===p.get('category'))?p.get('category'):'';$('examples').checked=p.get('labels')!=='0';$('selected-only').checked=p.get('selected')==='1';$('format').value=['png','svg'].includes(p.get('format'))?p.get('format'):'';$('transparent').checked=p.get('transparent')==='1';$('themeable').checked=p.get('themeable')==='1';
 if(/^#[0-9a-f]{6}$/i.test(p.get('accent')||''))$('accent').value=p.get('accent');setTheme(p.get('theme')||'blue',false);filter(false);const a=library.find(a=>a.id===p.get('asset'));if(a)openDetail(a,false);else if($('detail').open)$('detail').close();
}
function indexEntry(a){const fields=['id','title','kind','category','format','mime_type','transparent','width','height','canvas','render','path','preview_path','preview_has_example_labels','metadata_path','sha256','size_bytes','keywords'],row=Object.fromEntries(fields.map(k=>[k,a[k]]));Object.assign(row,{use_case:a.guidance.use_case,message:a.guidance.message,sample_data:Boolean(a.data?.is_sample)});if(a.composition)row.composition=a.composition;return row;}
async function publicAsset(a,resolved=theme,selectedMode=mode){
 const {download,...meta}=a,source={id:a.id,version:settings.project.version,raw_base:`https://raw.githubusercontent.com/${settings.project.repository}/v${settings.project.version}/`,path:a.path,preview_path:a.preview_path,preview_has_example_labels:a.preview_has_example_labels,sha256:a.sha256},path=`${a.format==='png'?'media':'assets'}/${fileName(a,selectedMode,resolved)}`;
 if(a.format==='png')return {...meta,source,path,preview_path:path,preview_has_example_labels:false,metadata_path:`metadata/${a.id}.json`};
 const svg=svgFor(a,resolved),bytes=new TextEncoder().encode(svg),digest=await crypto.subtle.digest('SHA-256',bytes);
 return {...meta,theme:resolved,source,size_bytes:bytes.length,sha256:[...new Uint8Array(digest)].map(v=>v.toString(16).padStart(2,'0')).join(''),labels:a.labels.map(l=>({...l,color:resolved.colors[l.color_role]})),path,preview_path:path,preview_has_example_labels:false,metadata_path:`metadata/${a.id}.json`};
}
async function pngBytes(a){
 let bytes=localMedia.get(a.path);
 if(!bytes){const response=await fetch(a.path);if(!response.ok)throw new Error('PNGを取得できませんでした。ページを再読み込みしてください。');bytes=new Uint8Array(await response.arrayBuffer());}
 const digest=await crypto.subtle.digest('SHA-256',bytes),hash=[...new Uint8Array(digest)].map(v=>v.toString(16).padStart(2,'0')).join('');
 if(hash!==a.sha256)throw new Error('PNGの内容が索引と一致しません。同じ版の一式ZIPを展開してください。');
 return bytes;
}

function saveBlob(blob,name){const a=element('a'),url=blobURL(blob);a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);}
async function savePack(items,button){
 if(button.disabled)return;
 if(!items.length){notify('保存する素材を選んでください。');return;}
 if(location.protocol==='file:'&&items.some(a=>a.format==='png'&&!localMedia.has(a.path))){notify('PNGをまとめて保存するには、展開したZIPのmediaフォルダを選択してください。');$('local-media').value='';$('local-media').click();return;}
 const packTheme=theme,packMode=mode,packName=themeName();button.disabled=true;const old=button.textContent;button.textContent='保存ファイルを準備中…';await new Promise(requestAnimationFrame);
 try{const records=await Promise.all(items.map(a=>publicAsset(a,packTheme,packMode))),payloads=await Promise.all(items.map(a=>a.format==='png'?pngBytes(a):Promise.resolve(svgFor(a,packTheme)))),files=items.flatMap((a,i)=>[{name:records[i].path,data:payloads[i]},{name:records[i].metadata_path,data:JSON.stringify(records[i],null,2)+'\n'}]);
 files.push({name:'catalog.json',data:JSON.stringify({...settings.project,asset_count:records.length,relative_paths:true,theme:packTheme,assets:records.map(indexEntry)},null,2)+'\n'},{name:'LICENSE-ASSETS',data:settings.assetLicense},{name:'README.txt',data:'PNGまたはSVGをPowerPointの［挿入］→［画像］から配置してください。\nmetadata/ に用途の例・描写の意味・形式・配色を収録しています。用途や配置は資料に合わせて選べます。数値は作例です。実データの生成は元リポジトリの llms.txt を参照してください。\n'});
 saveBlob(makeZip(files),`deckart-${packMode}-${items.length}.zip`);notify(`${items.length}点を保存しました。SVGの配色：${packName}。PNGは元の画像です。`);
 }catch(error){notify(error.message||'保存ファイルを作成できませんでした。素材を少なくして再試行してください。');}finally{button.disabled=false;button.textContent=old;}
}
for(const id of ['format','transparent','themeable'])$(id).addEventListener('change',()=>filter());
$('local-media').addEventListener('change',async e=>{let count=0;localMedia.clear();try{for(const file of e.target.files){const suffix=file.webkitRelativePath.split('/').slice(-2).join('/'),a=library.find(a=>a.format==='png'&&a.path==='media/'+suffix);if(a&&file.size===a.size_bytes){localMedia.set(a.path,new Uint8Array(await file.arrayBuffer()));count++;}}notify(count?`${count}点のPNGを読み込みました。もう一度、保存ボタンを押してください。`:'一致するPNGがありません。一式ZIPのmediaフォルダを選んでください。');}catch{notify('PNGを読み込めませんでした。mediaフォルダを選び直してください。');}});
$('search').addEventListener('input',()=>filter());$('category').addEventListener('change',()=>filter());$('selected-only').addEventListener('change',()=>filter());$('examples').addEventListener('change',()=>{if(active)$('detail-labels').checked=$('examples').checked;filter();});
$('detail-labels').addEventListener('change',e=>{$('examples').checked=e.target.checked;filter();});$('detail-palette').addEventListener('change',e=>{setTheme(e.target.value);if(mode==='brand')notify('ブランド色は素材一覧の色入力で指定できます。');});
for(const input of document.querySelectorAll('#palettes input'))input.addEventListener('change',()=>setTheme(input.value));
$('apply-accent').addEventListener('click',()=>setTheme('brand'));$('accent').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();setTheme('brand');}});
$('clear').addEventListener('click',()=>{$('search').value='';$('category').value='';$('format').value='';$('transparent').checked=false;$('themeable').checked=false;kind='';$('selected-only').checked=false;filter();$('search').focus();});
$('detail-select').addEventListener('click',()=>toggleSelected(active));$('unselect-all').addEventListener('click',()=>{selected.clear();updateSelection();filter();$('selected-only').focus();});
$('save-all').addEventListener('click',e=>savePack(library,e.currentTarget));$('save-selected').addEventListener('click',e=>savePack(library.filter(a=>selected.has(a.id)),e.currentTarget));
$('copy-metadata').addEventListener('click',async()=>{const a=library.find(a=>a.id===active),{download,...meta}=a,text=JSON.stringify({...meta,raw_base:`https://raw.githubusercontent.com/${settings.project.repository}/v${settings.project.version}/`},null,2);try{await navigator.clipboard.writeText(text);notify('検索情報をコピーしました。');}catch{saveBlob(new Blob([text],{type:'application/json'}),a.id.replace('/','--')+'.json');notify('検索情報をJSONで保存しました。');}});
$('detail').addEventListener('close',()=>{active=null;setHash();if(opener&&!opener.closest('article').hidden)opener.focus();});
$('json-download').href='catalog.json';
window.addEventListener('hashchange',restore);updateSelection();restore();
