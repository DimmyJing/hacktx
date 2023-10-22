<script lang="ts">
	import type { building } from '$lib/utils/buildings';
	import { Map, Marker } from 'mapbox-gl';
	import { createEventDispatcher, onDestroy, onMount } from 'svelte';

	export let lng: number;
	export let lat: number;
	export let buildings: building[];

	const dispatch = createEventDispatcher();

	const zoom = 18;

	let map: Map;
	let mapContainer: HTMLElement;

	$: if (map)
		map.panTo([lng, lat], {
			essential: true,
			duration: 1500
		});

	$: {
		if (map) {
			for (const location of buildings) {
				const el = document.createElement('img');
				el.src =
					'https://cdn.discordapp.com/attachments/1165122456000933919/1165421876596711465/Asset_22x.png';
				el.className = 'w-20 cursor-pointer';
				const marker = new Marker(el).setLngLat([location.lng, location.lat]);
				marker.addTo(map);
				marker.getElement().addEventListener('click', () => {
					dispatch('markerClick', {
						locationName: location.name
					});
				});
			}
		}
	}

	/*
	mapbox://styles/mapbox/streets-v11
	mapbox://styles/mapbox/outdoors-v11
	mapbox://styles/mapbox/light-v10
	mapbox://styles/mapbox/dark-v10
	mapbox://styles/mapbox/satellite-v9
	mapbox://styles/mapbox/satellite-streets-v11
	mapbox://styles/mapbox/navigation-day-v1
	mapbox://styles/mapbox/navigation-night-v1
	*/

	onMount(() => {
		map = new Map({
			container: mapContainer,
			accessToken: import.meta.env.VITE_MAPBOX_TOKEN,
			style: `mapbox://styles/mapbox/satellite-streets-v11`,
			center: [lng, lat],
			zoom: zoom
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>

<div class="absolute w-full h-full" bind:this={mapContainer} />
