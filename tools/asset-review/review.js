"use strict";
const el = id => document.getElementById(id);
const canvas = el("canvas"), ctx = canvas.getContext("2d");
const labels = {ref_starter_initial_final:"御三家 初期・最終の採用原画",ref_starter_middle:"御三家 中間形の提案",ref_early_wild_six:"一般種6体の採用原画",ref_field_topdown:"フィールドの採用方向",source_hanamimi_model_sheet_v01:"ハナミミ 設定画（形の方向採用・元の向き）",source_hanamimi_model_sheet_v02:"ハナミミ 設定画（背面を右上向きへ修正）",source_hanamimi_pixel_study_v01:"ハナミミ 前面・背面・アイコンの試作",runtime_hanamimi_front_v01:"ハナミミ 前面96px・採用済み",runtime_hanamimi_back_v01:"ハナミミ 背面96px・採用済み",runtime_hanamimi_icon_v01:"ハナミミ アイコン32px・採用済み",source_battle_ui_frame_v01:"戦闘UI枠・採用済みの元画像",runtime_battle_ui_frame_v01:"戦闘UI枠・採用済み",source_honoru_model_sheet_v01:"ホノル旧4肢案・不採用",source_honoru_model_sheet_v02:"ホノル 腕と翼が独立した設定画・基準採用",source_miomaru_model_sheet_v01:"ミオマル 前後横の設定画・基準採用",source_honoru_pixel_study_v01:"ホノル ドット絵用原画像",source_miomaru_pixel_study_v01:"ミオマル ドット絵用原画像",source_riscoro_model_sheet_v01:"リスコロ 前後横の設定画・採用済み",source_tsurumogu_model_sheet_v01:"ツルモグ 前後横の設定画・採用済み",source_haneri_model_sheet_v01:"ハネリ 前後横の設定画・採用済み",source_riscoro_pixel_study_v01:"リスコロ ドット絵用原画像",runtime_riscoro_front_v01:"リスコロ 前面96px・採用済み",runtime_riscoro_back_v01:"リスコロ 背面96px・採用済み",runtime_riscoro_icon_v01:"リスコロ アイコン32px・採用済み",source_tsurumogu_pixel_study_v01:"ツルモグ ドット絵用原画像",runtime_tsurumogu_front_v01:"ツルモグ 前面96px・採用済み",runtime_tsurumogu_back_v01:"ツルモグ 背面96px・採用済み",runtime_tsurumogu_icon_v01:"ツルモグ アイコン32px・採用済み",source_haneri_pixel_study_v01:"ハネリ ドット絵用原画像",runtime_haneri_front_v01:"ハネリ 前面96px・採用済み",runtime_haneri_back_v01:"ハネリ 背面96px・採用済み",runtime_haneri_icon_v01:"ハネリ アイコン32px・採用済み",runtime_honoru_front_v01:"ホノル 前面96px・採用済み",runtime_honoru_back_v01:"ホノル 背面96px・採用済み",runtime_honoru_icon_v01:"ホノル アイコン32px・採用済み",runtime_miomaru_front_v01:"ミオマル 前面96px・採用済み",runtime_miomaru_back_v01:"ミオマル 背面96px・採用済み",runtime_miomaru_icon_v01:"ミオマル アイコン32px・採用済み",source_mizutta_model_sheet_v01:"ミズッタ 前後横の設定画・確認待ち",source_cocoil_model_sheet_v01:"ココイル 前後横の設定画・確認待ち",source_yorumiru_model_sheet_v01:"ヨルミル旧6肢案・不採用",source_yorumiru_model_sheet_v02:"ヨルミル 四肢へ修正した設定画・確認待ち"};
let entries = [], current = null, currentTitle = "", sourceRole = "", loadSequence = 0;
const specs = {front:[96,96,4],back:[96,96,4],icon:[32,32,2],walk:[96,192,0]};
function line(text, className="") {const p=document.createElement("p");p.textContent=text;p.className=className;el("results").append(p);}
function redraw() {
  if (!current) return;
  const w=current.naturalWidth,h=current.naturalHeight,kind=el("kind").value,spec=specs[kind];
  const zoom=el("zoom").value === "fit" ? Math.min(1,(el("stage").clientWidth-34)/w,(el("stage").clientHeight-34)/h) : Number(el("zoom").value);
  canvas.width=w;canvas.height=h;canvas.style.width=`${Math.max(1,w*zoom)}px`;canvas.style.height=`${Math.max(1,h*zoom)}px`;
  ctx.drawImage(current,0,0);
  const pixels=ctx.getImageData(0,0,w,h).data;
  let transparent=0,partial=0,minX=w,minY=h,maxX=-1,maxY=-1;
  for(let y=0;y<h;y++)for(let x=0;x<w;x++) {const alpha=pixels[(y*w+x)*4+3];if(alpha===0)transparent++;else{if(alpha<255)partial++;minX=Math.min(x,minX);minY=Math.min(y,minY);maxX=Math.max(x,maxX);maxY=Math.max(y,maxY);}}
  el("name").textContent=currentTitle;el("size").textContent=`${w} × ${h} px`;
  el("stage").dataset.background=el("background").value;el("results").replaceChildren();
  line(sourceRole);
  line(`完全透明 ${transparent} px ／ 半透明 ${partial} px`);
  if(!spec) line("参照資料として表示中。取り込み用画像の合否は判定しません。");
  else {
    const [expectedW,expectedH,pad]=spec, dimensionsOK=w===expectedW&&h===expectedH;
    line(dimensionsOK?"寸法：規格案と一致":"寸法：規格案と不一致",dimensionsOK?"good":"attention");
    line(transparent>0?"透過：透明ピクセルあり":"透過：透明ピクセルなし",transparent>0?"good":"attention");
    const empty=maxX<0;
    if(empty) line("描画内容：全透明。素材として使えません。","attention");
    if(!empty&&pad) {const marginOK=minX>=pad&&minY>=pad&&maxX<w-pad&&maxY<h-pad;line(marginOK?`外周：${pad}px以上の透明域あり`:`外周：${pad}pxの透明域が不足`,marginOK?"good":"attention");}
    if(kind==="walk")line("歩行：12コマの接地・向き・歩幅は目視確認が必要です。");
    if(spec&&el("guides").checked&&dimensionsOK) {
      ctx.strokeStyle="#d94278";ctx.lineWidth=1;
      if(pad)ctx.strokeRect(pad+.5,pad+.5,w-2*pad-1,h-2*pad-1);
      const anchors=kind==="walk"?Array.from({length:12},(_,i)=>[(i%3)*32+16,Math.floor(i/3)*48+44]):[[w/2,kind==="icon"?h-2:88]];
      for(const [x,y] of anchors){ctx.beginPath();ctx.moveTo(x-3,y+.5);ctx.lineTo(x+3,y+.5);ctx.moveTo(x+.5,y-3);ctx.lineTo(x+.5,y+3);ctx.stroke();}
      if(kind==="walk") {for(let x=32;x<w;x+=32){ctx.beginPath();ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,h);ctx.stroke();}for(let y=48;y<h;y+=48){ctx.beginPath();ctx.moveTo(0,y+.5);ctx.lineTo(w,y+.5);ctx.stroke();}}
    }
  }
  if(el("grid").checked&&zoom>=4&&w<=512&&h<=512){ctx.strokeStyle="#45645040";ctx.lineWidth=.15;for(let x=0;x<w;x++){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}for(let y=0;y<h;y++){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}}
}
async function showBlob(blob,title,role) {
  const ticket=++loadSequence;
  // Reject SVG or a renamed non-PNG file; only raster PNG belongs in this viewer.
  const signature=new Uint8Array(await blob.slice(0,8).arrayBuffer());
  if(signature.join(",")!=="137,80,78,71,13,10,26,10")throw new Error("PNG形式の画像を選んでください。");
  // Bound decode and canvas allocation for accidental huge uploads.
  const header=new DataView(await blob.slice(0,24).arrayBuffer());
  if(header.byteLength<24||header.getUint32(16)*header.getUint32(20)>16000000)throw new Error("画像は1600万画素以下にしてください。");
  const url=URL.createObjectURL(blob),img=new Image();
  try {await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(new Error("PNGを読み込めませんでした。"));img.src=url;});
    if(ticket!==loadSequence)return;current=img;currentTitle=title;sourceRole=role;redraw();
  } finally {URL.revokeObjectURL(url);}
}
function failed(e){el("results").replaceChildren();line(e.message,"attention");}
async function chooseRecorded() {
  const entry=entries.find(x=>x.id===el("asset").value);if(!entry)return;
  el("kind").value=entry.kind || "reference";el("provenance").textContent=entry.path;
  try{const response=await fetch("../../"+entry.path);if(!response.ok)throw new Error("画像が見つかりません。");await showBlob(await response.blob(),labels[entry.id]||entry.id,entry.state==="rejected_anatomy_superseded"?"不採用の旧案。現在の制作基準には使いません。":entry.role==="runtime_image"?"取り込み用静止素材・見た目と画像規格を確認済み。":entry.role==="runtime_candidate"?"取り込み候補・見た目の確認待ち。":"参照資料・ゲーム取り込み用ではありません。");}catch(e){failed(e);}
}
el("upload").addEventListener("change",async()=>{const f=el("upload").files[0];if(!f)return;el("provenance").textContent="手元の候補（未登録）";try{await showBlob(f,f.name,"制作候補・未採用。規格案を選んで照合してください。");}catch(e){failed(e);}});
el("asset").addEventListener("change",chooseRecorded);
for(const id of ["kind","zoom","background","guides","grid"])el(id).addEventListener("change",redraw);
window.addEventListener("resize",redraw);
(async()=>{try{const response=await fetch("../../manifests/assets.json");if(!response.ok)throw new Error("台帳を取得できません。READMEの起動手順でHTTPサーバーを起動してください。");const manifest=await response.json();entries=manifest.entries.filter(x=>x.path.endsWith(".png"));el("asset").replaceChildren(...entries.map(entry=>{const option=document.createElement("option");option.value=entry.id;option.textContent=labels[entry.id]||entry.id;return option;}));el("asset").value="runtime_hanamimi_front_v01";await chooseRecorded();}catch(e){failed(e);}})();
