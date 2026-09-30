'use strict';
// Keep this small deterministic search contract in parity with scripts/search.py.
const DeckArtSearch=(()=>{
 const normalize=value=>String(value).normalize('NFKC').toLowerCase().trim();
 const escape=value=>value.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 function contains(text,term){if(term.length===1)return text.split(/\s+/).includes(term);return /^[a-z0-9][a-z0-9 ._-]*$/.test(term)?new RegExp('(^|[^a-z0-9])'+escape(term)+'($|[^a-z0-9])').test(text):text.includes(term);}
 function occurrences(text,term){
  if(!term)return [];
  const result=[],ascii=/^[a-z0-9][a-z0-9 ._-]*$/.test(term);let start=0;
  while((start=text.indexOf(term,start))>=0){
   const end=start+term.length,before=text[start-1]||'',after=text[end]||'';
   const valid=term.length===1?(!before||/\s/.test(before))&&(!after||/\s/.test(after)):!ascii||!(/[a-z0-9]/.test(before)||/[a-z0-9]/.test(after));
   if(valid)result.push([start,end]);start++;
  }
  return result;
 }
 function fields(asset,config){
  const guide=asset.guidance||{},words=Object.values(asset.composition||{}).flatMap(value=>[String(value),...(config.composition_terms[String(value)]||[])]);
  return [[asset.id.split('/').slice(1).join('/'),8],[asset.title,12],[asset.keywords.join(' '),6],[asset.use_case??guide.use_case??'',3],[asset.message??guide.message??'',7],[config.kind_terms[asset.kind].join(' '),8],[words.join(' '),2],[asset.category||'',3]].map(([text,weight])=>[normalize(text),weight]);
 }
 function prepare(assets,config){
  const documents=assets.map(asset=>[asset,fields(asset,config)]),groups=[...config.groups,...Object.values(config.kind_terms)].map(group=>group.map(normalize)),aliases=new Set(groups.flat()),vocabulary=new Set();
  for(const asset of assets)for(const word of [asset.title,...asset.keywords,...asset.id.split(/[-/]/)]){const term=normalize(word);if(term.length>=2&&!aliases.has(term))vocabulary.add(term);}
  return {documents,groups,vocabulary:[...vocabulary].sort(),config,matches:new Map()};
 }
 function queryTerms(query,prepared){
  query=normalize(query);const candidates=[...prepared.groups,...prepared.vocabulary.map(word=>[word])].map(group=>[group,group.flatMap(word=>occurrences(query,word))]).filter(([,spans])=>spans.length),spans=candidates.flatMap(([,matches])=>matches);
  // Preserve independently occurring words, but do not count the fragments of
  // a longer phrase as additional topics.
  const uncovered=spans.filter(([start,end])=>!spans.some(([left,right])=>(left!==start||right!==end)&&left<=start&&end<=right));
  const groups=candidates.filter(([,matches])=>matches.some(([start,end])=>uncovered.some(([left,right])=>left===start&&right===end))).map(([group])=>group),generic=new Set(prepared.config.generic_terms.map(normalize)),specific=groups.filter(group=>!group.every(word=>generic.has(word)));
  return specific.length?specific:groups;
 }
 function interleave(entries,kindOrder){
  const kinds=[...kindOrder,...[...new Set(entries.map(asset=>asset.kind))].filter(kind=>!kindOrder.includes(kind)).sort()],queues=kinds.map(kind=>entries.filter(asset=>asset.kind===kind).sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0)),result=[];
  while(queues.some(queue=>queue.length))for(const queue of queues)if(queue.length)result.push(queue.shift());return result;
 }
 function rank(prepared,query,filters={}){
  const normalized=normalize(query),terms=queryTerms(query,prepared),buckets=new Map();
  const columns=terms.map(group=>{
   const key=JSON.stringify(group);if(!prepared.matches.has(key))prepared.matches.set(key,prepared.documents.map(([,document])=>Math.max(0,...document.filter(([text])=>group.some(word=>contains(text,word))).map(([,weight])=>weight))));return prepared.matches.get(key);
  });
  const matched=prepared.documents.map((_,i)=>columns.map(column=>column[i])),broad=new Set(prepared.config.broad_terms),specific=terms.some(group=>!group.some(word=>broad.has(word))),factors=terms.map(group=>specific&&group.some(word=>broad.has(word))?1:3);
  const rarity=terms.map((_,i)=>{const value=Math.floor(1000/(20+matched.filter(matches=>matches[i]).length));return factors[i]===1?Math.min(value,10):value;});
  for(let i=0;i<prepared.documents.length;i++){
   const asset=prepared.documents[i][0],matches=matched[i];
   if(['kind','format','category','transparent'].some(key=>key in filters&&asset[key]!==filters[key])||('themeable' in filters&&asset.render.theme!==filters.themeable))continue;
   const exactId=normalized===normalize(asset.id),exactTitle=normalized===normalize(asset.title),partialTitle=normalized.length>=2&&normalize(asset.title).includes(normalized);
   if(normalized&&!exactId&&!exactTitle&&!partialTitle&&!matches.some(Boolean))continue;
   const score=matches.reduce((sum,weight,index)=>sum+weight*rarity[index]*factors[index],0)+(exactId?2000000:exactTitle?1000000:partialTitle?12:0);if(!buckets.has(score))buckets.set(score,[]);buckets.get(score).push(asset);
  }
  return {assets:[...buckets.keys()].sort((a,b)=>b-a).flatMap(score=>interleave(buckets.get(score),prepared.config.kind_order)),terms:terms.map(group=>group[0])};
 }
 return {prepare,rank};
})();
if(typeof module!=='undefined'&&module.exports)module.exports=DeckArtSearch;
