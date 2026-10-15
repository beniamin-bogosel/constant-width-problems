// Render mathematical fragments during export, so reading needs no network or math JS.
const katex = require('./vendor/katex/katex.min.js');
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const fragments = JSON.parse(input);
    const result = fragments.map(({text, display}) => katex.renderToString(text, {
      displayMode: display, throwOnError: true, trust: false, strict: 'error',
      output: 'htmlAndMathml'
    }));
    process.stdout.write(JSON.stringify(result));
  } catch (error) { console.error(String(error)); process.exitCode = 1; }
});
