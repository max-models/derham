/** Prefix a site-root-relative path ("/tutorials/foo/") with the site's base path. */
export function withBase(path: string): string {
	if (/^[a-z]+:\/\//.test(path)) return path;
	return import.meta.env.BASE_URL.replace(/\/$/, '') + (path.startsWith('/') ? path : `/${path}`);
}
