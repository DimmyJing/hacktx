import { writable } from 'svelte/store';

type building = {
	lng: number;
	lat: number;
	name: string;
	image: string;
	markerType: 'SCHOOL' | 'RESIDENTIAL' | 'OTHER';
	significance: string;
	dailyActiveUsers: number;
	contributors: {
		uid: string;
		name: string;
		title: string;
		avatar: string;
		activeHour: number;
	}[];
};

export const buildingStore = writable<building[]>([]);
