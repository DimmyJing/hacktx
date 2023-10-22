function toVal(mix: unknown, results: string[]) {
	if (typeof mix === 'string') {
		results.push(mix);
	} else if (typeof mix === 'number') {
		results.push(mix.toString());
	} else if (typeof mix === 'object') {
		if (Array.isArray(mix)) {
			for (const item of mix) {
				if (item) toVal(item, results);
			}
		} else if (mix !== null) {
			for (const [key, val] of Object.entries(mix)) {
				if (val) toVal(key, results);
			}
		}
	}
}

export function clsx(...args: unknown[]) {
	const results: string[] = [];
	for (const arg of args) {
		toVal(arg, results);
	}
	return results.join(' ');
}

export default clsx;
