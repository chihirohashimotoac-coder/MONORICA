"use strict";
// Asset-layout preview only. No combat, state progression, saves or services.
const ROOT = "../../";
const FONT = '16px "BattleDot"';
const canvas = document.getElementById("battle");
const ctx = canvas.getContext("2d");

async function loadJSON(path) {
  const response = await fetch(ROOT + path);
  if (!response.ok) throw new Error("UIの資料を読み込めませんでした：" + path);
  return response.json();
}
async function loadImage(path) {
  const image = new Image();
  image.src = ROOT + path;
  await image.decode();
  return image;
}
function pixelBox(context, x, y, w, h, cut, fill) {
  context.fillStyle = fill;
  context.fillRect(x + cut, y, w - 2 * cut, h);
  context.fillRect(x, y + cut, w, h - 2 * cut);
  if (cut > 1) {
    context.fillRect(x + 1, y + 1, w - 2, h - 2);
  }
}
function oval(context, cx, cy, rx, ry, color) {
  context.fillStyle = color;
  for (let dy = -ry; dy <= ry; dy++) {
    const half = Math.floor(rx * Math.sqrt(1 - dy * dy / (ry * ry)));
    context.fillRect(cx - half, cy + dy, half * 2 + 1, 1);
  }
}
function statusFrame(context, rect, palette) {
  const [x, y, w, h] = rect;
  pixelBox(context, x + 3, y + 3, w, h, 4, "#6c8061");
  pixelBox(context, x, y, w, h, 4, palette.ink);
  pixelBox(context, x + 2, y + 2, w - 4, h - 4, 3, palette.olive_border);
  pixelBox(context, x + 4, y + 4, w - 8, h - 8, 2, palette.status_face);
}
function dialogueFrame(context, rect, face, palette, command = false) {
  const [x, y, w, h] = rect;
  pixelBox(context, x, y, w, h, 4, "#303e43");
  pixelBox(context, x + 2, y + 2, w - 4, h - 4, 3, "#afb6ae");
  pixelBox(context, x + 5, y + 5, w - 10, h - 10, 2, command ? "#727b70" : palette.gold_trim);
  pixelBox(context, x + 8, y + 8, w - 16, h - 16, 1, face);
}
function hpTrack(context, x, y, width) {
  pixelBox(context, x, y, width, 8, 1, "#394b40");
  context.fillStyle = "#f8f6db";
  context.fillRect(x + 2, y + 2, width - 4, 4);
}
function drawFrames(context, layout) {
  const p = layout.palette, r = layout.rects;
  statusFrame(context, r.enemy_status, p);
  statusFrame(context, r.ally_status, p);
  hpTrack(context, 74, 46, 100);
  hpTrack(context, 252, 141, 112);
  dialogueFrame(context, r.message, p.message_face, p);
  dialogueFrame(context, r.commands, p.menu_face, p, true);
  context.fillStyle = "#596b70";
  context.fillRect(250, 167, 114, 3);
}
const textCache = new Map();
function pixelText(context, value, x, y, color, shadow = false) {
  // Rasterise the local font on its native 16px grid, then remove soft alpha.
  // The exported frame PNG has no text; this remains editable UI content.
  const key = value + color;
  if (!textCache.has(key)) {
    const layer = document.createElement("canvas");
    const local = layer.getContext("2d");
    local.font = FONT;
    layer.width = Math.ceil(local.measureText(value).width) + 2;
    layer.height = 18;
    local.font = FONT;
    local.textBaseline = "alphabetic";
    local.fillStyle = color;
    local.fillText(value, 0, 14);
    const pixels = local.getImageData(0, 0, layer.width, layer.height);
    for (let i = 3; i < pixels.data.length; i += 4) pixels.data[i] = pixels.data[i] >= 128 ? 255 : 0;
    local.putImageData(pixels, 0, 0);
    textCache.set(key, layer);
  }
  const layer = textCache.get(key);
  if (shadow) {
    // A one-pixel dark echo, only on the dialogue's pale glyphs.
    pixelText(context, value, x + 1, y + 1, "#173c50");
  }
  context.drawImage(layer, x, y);
}
function hpFill(context, x, y, width, ratio) {
  const pixels = Math.round((width - 4) * Math.max(0, Math.min(1, ratio)));
  context.fillStyle = "#4bbe83";
  context.fillRect(x + 2, y + 2, pixels, 4);
  context.fillStyle = "#89dc9f";
  context.fillRect(x + 2, y + 2, pixels, 1);
}
function cursor(context, x, y) {
  context.fillStyle = "#303d35";
  for (let row = 0; row < 11; row++) context.fillRect(x, y + row, 6 - Math.abs(row - 5), 1);
}

async function main() {
  const [layout, strings] = await Promise.all([
    loadJSON("content/ui/battle-ui-layout.json"),
    loadJSON("content/ui/battle-ui-ja.json")
  ]);
  const catalog = window.StarterPreviewCatalog;
  const query = new URLSearchParams(window.location.search);
  const choices = {};
  for (const role of ["ally", "enemy"]) {
    const key = Object.hasOwn(catalog, query.get(role)) ? query.get(role) : "hanamimi";
    choices[role] = catalog[key];
    const select = document.getElementById(role + "-preview");
    select.replaceChildren(...Object.entries(catalog).map(([value, entry]) => {
      const option = document.createElement("option");option.value = value;option.textContent = entry.name;return option;
    }));
    select.value = key;
    select.addEventListener("change", () => {
      const url = new URL(window.location.href);
      url.searchParams.set(role, select.value);
      window.location.href = url.href;
    });
    layout.sprites[role].path = "assets/runtime/monsters/" + catalog[key].id + (role === "ally" ? "/back.png" : "/front.png");
    layout.preview_values[role].name = catalog[key].name;
  }
  document.getElementById("heading").textContent = choices.ally.name + "の戦闘UI";
  canvas.setAttribute("aria-label", "左下に味方の" + choices.ally.name + "の背面、右上に相手の" + choices.enemy.name + "の正面。採用済みのひらがなコマンドと情報欄。");
  if (choices.ally.id !== "starter_flower_hare_01" || choices.enemy.id !== "starter_flower_hare_01") {
    const pending = [...new Set(Object.values(choices).filter(entry => entry.review !== "adopted").map(entry => entry.name))];
    document.getElementById("preview-note").textContent = "素材確認のため2体を仮配置しています。" + (pending.length ? pending.join("・") + "の新しいドット画像は見た目確認待ち。" : "表示している静止素材は見た目採用済み。") + "レベル・HP・経験値は表示例で、種族データではありません。操作・戦闘の機能はまだありません。";
  }
  const loaded = await document.fonts.load(FONT, "ハナミミ たたかう");
  if (!loaded.length) throw new Error("ドット字体を読み込めませんでした。");
  const [enemy, ally] = await Promise.all([
    loadImage(layout.sprites.enemy.path), loadImage(layout.sprites.ally.path)
  ]);
  canvas.width = layout.viewport.width;
  canvas.height = layout.viewport.height;
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = "#e0ecb7";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.beginPath();ctx.rect(0, 0, canvas.width, layout.viewport.field_bottom);ctx.clip();
  const sky = ctx.createLinearGradient(0, 0, 0, layout.viewport.field_bottom);
  sky.addColorStop(0, "#bfdcde");sky.addColorStop(.65, "#e7efd0");sky.addColorStop(1, "#dcecb2");
  ctx.fillStyle = sky;ctx.fillRect(0, 0, canvas.width, layout.viewport.field_bottom);
  ctx.fillStyle = "#eef6e960";
  for (let y = 2; y < layout.viewport.field_bottom; y += 3) ctx.fillRect(0, y, canvas.width, 1);
  oval(ctx, 294, 109, 74, 21, "#d5e88a");
  oval(ctx, 294, 109, 66, 17, "#c0d986");
  oval(ctx, 294, 109, 57, 13, "#b9d58a");
  oval(ctx, 100, 177, 98, 26, "#bdd17d");
  oval(ctx, 100, 177, 88, 21, "#adc781");
  for (const [name, image] of [["enemy", enemy], ["ally", ally]]) {
    const rect = layout.sprites[name];
    ctx.drawImage(image, rect.x, rect.y, rect.width, rect.height);
  }
  ctx.restore();
  drawFrames(ctx, layout);
  const preview = layout.preview_values;
  hpFill(ctx, 74, 46, 100, preview.enemy.hp_ratio);
  hpFill(ctx, 252, 141, 112, preview.ally.hp / preview.ally.max_hp);
  pixelText(ctx, preview.enemy.name, 28, 28, "#354137");
  pixelText(ctx, "Lv" + preview.enemy.level, 138, 28, "#354137");
  pixelText(ctx, "HP", 52, 42, "#b18f31");
  pixelText(ctx, preview.ally.name, 212, 123, "#354137");
  pixelText(ctx, "Lv" + preview.ally.level, 328, 123, "#354137");
  pixelText(ctx, "HP", 230, 138, "#b18f31");
  pixelText(ctx, preview.ally.hp + " / " + preview.ally.max_hp, 292, 151, "#354137");
  ctx.fillStyle = "#59a8cf";
  ctx.fillRect(251, 168, Math.round(112 * preview.ally.experience_ratio), 1);
  const message = strings.messages.choose_action.replace("{name}", preview.ally.name).split("\n");
  message.forEach((line, index) => pixelText(ctx, line, 20, 192 + index * 27, "#fffde8", true));
  const commands = strings.commands;
  for (const [label, x, y] of [[commands.fight, 233, 191], [commands.bag, 314, 191], [commands.party, 233, 220], [commands.run, 314, 220]]) pixelText(ctx, label, x, y, "#354137");
  cursor(ctx, 222, 194);
  window.BattleUI = {
    ready: true,
    layout,
    strings,
    exportPreview(scale = 3) {
      const output = document.createElement("canvas");
      output.width = canvas.width * scale;output.height = canvas.height * scale;
      const context = output.getContext("2d");context.imageSmoothingEnabled = false;
      context.drawImage(canvas, 0, 0, output.width, output.height);
      return output.toDataURL("image/png");
    },
    exportFrameLayer() {
      const output = document.createElement("canvas");output.width = canvas.width;output.height = canvas.height;
      drawFrames(output.getContext("2d"), layout);
      return output.toDataURL("image/png");
    }
  };
  document.getElementById("loading").hidden = true;
}
main().catch(error => {
  document.getElementById("loading").textContent = error.message;
  window.BattleUI = {ready: false, error: error.message};
});
