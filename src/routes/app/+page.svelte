<script lang="ts">
	import Map from './map.svelte';
	import Building from './building.svelte';
	import { onMount } from 'svelte';

	let locationIdx = 0;
	let targetLocation = -1;

	const locations: {
		lng: number;
		lat: number;
		name: string;
		image: string;
	}[] = [
		{
			lat: 30.28667289666327,
			lng: -97.73766242199612,
			name: 'Welch Hall',
			image:
				'https://cdn.discordapp.com/attachments/1165122456000933919/1165415593760006216/AF1QipPC91wIbLsE-wNvRhZls8zHPuLng_n8QnN0ToDZw408-h306-k-no.png'
		},
		{
			lat: 30.284867,
			lng: -97.732414,
			name: 'Memorial Stadium',
			image:
				'https://cdn.discordapp.com/attachments/1165122456000933919/1165413862896566302/AF1QipNQQAN0jLEN1gaZUsNjPEholYqJtdIigJ7eA-4pw408-h306-k-no.png'
		},
		{
			lat: 30.286496,
			lng: -97.739515,
			name: 'UT Tower',
			image:
				'https://cdn.discordapp.com/attachments/1165122456000933919/1165414179704938658/AF1QipMYkiXIYsSh2u05k0ZINRtFarkR4pp6E_bETI8Aw408-h306-k-no.png'
		},
		{
			lat: 30.287431,
			lng: -97.742657,
			name: 'The Castillian',
			image:
				'https://cdn.discordapp.com/attachments/1165122456000933919/1165414638297554994/AF1QipPXFwYhP4bey9pf4nB42f8Bmn0dmysRTTR39IJaw408-h275-k-no.png'
		}
	];

	let locationRefs: HTMLElement[] = locations.map(() => null as unknown as HTMLElement);
	let locationRef: HTMLDivElement;

	onMount(() => {});

	function markerClick(e: CustomEvent<{ locationName: string }>) {
		locationIdx = locations.findIndex((location) => location.name === e.detail.locationName);
		targetLocation = locationIdx;
		locationRef.scrollTo({
			left: locationIdx * locationRef.offsetWidth,
			behavior: 'smooth'
		});
	}

	function onScroll() {
		const currLocation = Math.round(locationRef.scrollLeft / locationRef.offsetWidth);
		if (currLocation !== locationIdx && targetLocation === -1) {
			locationIdx = currLocation;
		} else if (currLocation === targetLocation) {
			targetLocation = -1;
		}
	}
</script>

<div class="flex flex-row w-screen h-screen">
	<Map
		lng={locations[locationIdx].lng}
		lat={locations[locationIdx].lat}
		{locations}
		on:markerClick={markerClick}
	/>
	<div class="absolute right-0 w-[40vw] h-full">
		<div
			class="m-10 bg-slate-50 h-[90%] rounded-2xl border-2 shadow-xl border-white snap-x overflow-x-scroll flex flex-row snap-mandatory no-scrollbar"
			on:scroll={onScroll}
			bind:this={locationRef}
		>
			{#each locations as location, idx}
				<Building {location} bind:ref={locationRefs[idx]} />
			{/each}
		</div>
	</div>
</div>
