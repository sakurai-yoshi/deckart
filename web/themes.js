'use strict';
// Mirrors scripts/themes.py. Parity is checked against exported SVG metadata.
window.resolveTheme=function resolveTheme(accent='#2864F0',monochrome=false){
 const rgb=c=>{if(!/^#[0-9a-f]{6}$/i.test(c))throw new Error('色は #005BAC のように6桁で入力してください。');return [1,3,5].map(i=>parseInt(c.slice(i,i+2),16));};
 const hex=a=>'#'+a.map(v=>Math.min(255,Math.max(0,Math.floor(v+.5))).toString(16).padStart(2,'0')).join('').toUpperCase();
 const mix=(a,b,t)=>hex(rgb(a).map((v,i)=>v*(1-t)+rgb(b)[i]*t));
 const luminance=c=>rgb(c).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
 const contrast=(a,b='#FFFFFF')=>(Math.max(luminance(a),luminance(b))+.05)/(Math.min(luminance(a),luminance(b))+.05);
 const requested=hex(rgb(accent));
 if(monochrome)return {mode:'monochrome',colors:{ink:'#202A35',accent:'#202A35',mid:'#929BA6',pale:'#E8EBEE',faint:'#F5F6F7',muted:'#596370',paper:'#FFFFFF',positive:'#202A35',negative:'#202A35',caution:'#202A35',caution_pale:'#E8EBEE',series_secondary:'#63707F'},adjustments:[]};
 let effective=requested;
 for(let step=1;step<256;step++){if(contrast(effective)>=4.5)break;effective=mix(requested,'#000000',step/255);}
 const tones=requested==='#2864F0'?{mid:'#79A7ED',pale:'#E7F0FF',faint:'#F3F7FD'}:{mid:mix(effective,'#FFFFFF',.68),pale:mix(effective,'#FFFFFF',.9),faint:mix(effective,'#FFFFFF',.965)};
 return {mode:'brand',requested_accent:requested,colors:{ink:'#153A6B',muted:'#607590',paper:'#FFFFFF',positive:'#137D66',negative:'#B5473A',caution:'#A46A16',caution_pale:'#FFF0D7',series_secondary:contrast(effective,'#153A6B')>=1.6?'#153A6B':'#63707F',...tones,accent:effective},adjustments:requested===effective?[]:[`Accent adjusted from ${requested} to ${effective} for white-mark contrast.`]};
};
window.themeSVG=function themeSVG(source,theme){
 const document=new DOMParser().parseFromString(source,'image/svg+xml');
 for(const el of document.querySelectorAll('[data-fill-role],[data-stroke-role]'))for(const paint of ['fill','stroke']){
  const role=el.getAttribute('data-'+paint+'-role');if(role)el.setAttribute(paint,theme.colors[role]);
 }
 return new XMLSerializer().serializeToString(document.documentElement)+'\n';
};
