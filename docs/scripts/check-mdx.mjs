// Compile every MDX page under src/content/docs with the site's markdown plugins and report the
// files that do not parse, with the line and the message. Runs in seconds, so a broken notebook
// conversion is found before the (slow) site build.
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { compile } from '@mdx-js/mdx';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const root = new URL('..', import.meta.url).pathname;
const content = join(root, 'src', 'content', 'docs');

function* walk(directory) {
	for (const name of readdirSync(directory)) {
		const path = join(directory, name);
		if (statSync(path).isDirectory()) yield* walk(path);
		else if (name.endsWith('.mdx')) yield path;
	}
}

let failures = 0;
let count = 0;
for (const file of walk(content)) {
	count += 1;
	const source = readFileSync(file, 'utf8').replace(/^---\n[\s\S]*?\n---\n/, (front) =>
		'\n'.repeat(front.split('\n').length - 1)
	);
	try {
		await compile(source, { remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex] });
	} catch (error) {
		failures += 1;
		const where = error.line ? `:${error.line}:${error.column ?? 0}` : '';
		console.error(`${relative(root, file)}${where}: ${error.reason ?? error.message}`);
	}
}
console.log(`[check-mdx] ${count - failures} of ${count} MDX files compile`);
if (failures) process.exit(1);
