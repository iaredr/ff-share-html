# Media inventory for redesign

## Videos (playable in browser — do NOT replace with still frames)
- media/hk-plaza/video/plaza-buffet.mp4 — 香港环亚自助餐台
- media/hk-plaza/video/plaza-meal.mp4 — 香港环亚托盘餐

## User photos (keep captions; clickable lightbox)
- media/beijing/beijing-1..5.jpg — 北京机场（部分仅 512px HEIC 解码上限）
- media/delta-priority/delta-1..3.jpg — 达美优先行李
- media/sanjose/sanjose-1.jpg — 行李到了 San Jose
- media/nz-lounge/nz-1..4.jpg — 新西兰休息室
- media/taipei/taipei-1..3.jpg — 台北休息室（担担面彩蛋口播）

## oneworld
- logos: oneworld.svg, cathay.svg, qantas.svg, aa-symbol.svg, aa-wordmark.svg
- planes: cx-oneworld.jpg, qantas-plane.jpg, aa-plane.jpg
- emerald-sapphire.png — 旧示意图（已弃用：P18 改为 s18.html 内联 SVG 卡片）

## SkyTeam (need many on that slide)
- skyteam-livery.jpg, mu-chinaeastern.jpg, mf-xiamen.jpg, ci-chinaairlines.jpg, dl-delta.jpg

## Star Alliance
- star-livery.jpg, ca-airchina.jpg, zh-shenzhen.jpg, br-eva.jpg, sq-singapore.jpg, lh-lufthansa.jpg, nz-airnz.jpg, ua-united.jpg

## 待补原图（当前为纯黑 jpg，HEIC 解码失败）
delta-priority/delta-1.jpg, delta-2.jpg, sanjose/sanjose-1.jpg, nz-lounge/nz-1..4.jpg
页面上显示「原图待补」占位。替换文件后，去 build/parts 对应 sNN.html 删掉该 .fig 的 `data-pending`，再 `python3 build/build.py` 重新生成 index.html。
