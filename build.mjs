// app.html(아티팩트용 조각)을 Netlify용 완전한 HTML(site/index.html)로 감싸기
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
const src = readFileSync(new URL('./app.html', import.meta.url), 'utf8');
const cut = src.indexOf('</style>') + '</style>'.length;
const headPart = src.slice(0, cut), body = src.slice(cut);
const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1A2350">
${headPart}
</head>
<body>
${body}
</body>
</html>
`;
mkdirSync(new URL('./site/', import.meta.url), { recursive: true });
writeFileSync(new URL('./site/index.html', import.meta.url), html);
console.log('site/index.html', html.length, 'bytes');
