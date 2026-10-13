// Keep guide pages available when Astro is launched directly through npm.
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const repo = new URL('../../', import.meta.url);
const localPython = fileURLToPath(
	new URL(process.platform === 'win32' ? '.venv/Scripts/python.exe' : '.venv/bin/python', repo)
);
const python = process.env.DOCS_PYTHON ||
	(existsSync(localPython) ? localPython : process.platform === 'win32' ? 'python' : 'python3');
const commands = process.argv.includes('--execute') ? [['execute'], ['convert', '--strict']] : [['convert']];
for (const command of commands) {
	const result = spawnSync(python, [fileURLToPath(new URL('docs/tools/notebooks.py', repo)), ...command], {
		cwd: fileURLToPath(repo),
		stdio: 'inherit',
	});
	if (result.error) {
		console.error(`[notebooks] Could not run ${python}: ${result.error.message}`);
		console.error('Set DOCS_PYTHON to the Python interpreter used for the docs.');
	}
	if (result.status !== 0) process.exit(result.status ?? 1);
}
