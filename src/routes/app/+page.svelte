<script lang="ts">
	import Map from './map.svelte';
	import Building from './building.svelte';
	import { onMount } from 'svelte';
	import { createQuery } from '@tanstack/svelte-query';
	import axios from 'axios';
	import { buildingStore, type building } from '$lib/utils/buildings';

	let locationIdx = 0;
	let targetLocation = -1;

	const query = createQuery({
		queryKey: ['buildings'],
		queryFn: () => axios.get<building[]>('http://localhost:8000/buildings')
	});

	$: if ($query.data?.data) {
		buildingStore.set($query.data.data);
	}

	let locationRefs: HTMLElement[];
	$: if ($buildingStore.length > 0) {
		locationRefs = $buildingStore.map(() => null as unknown as HTMLElement);
	}
	let locationRef: HTMLDivElement;

	onMount(() => {});

	function markerClick(e: CustomEvent<{ locationName: string }>) {
		locationIdx = $buildingStore.findIndex((location) => location.name === e.detail.locationName);
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

{#if $query.isLoading}
	<span>Loading...</span>
{:else}
	<div class="flex flex-row w-screen h-screen">
		<Map
			lng={$buildingStore[locationIdx].lng}
			lat={$buildingStore[locationIdx].lat}
			buildings={$buildingStore}
			on:markerClick={markerClick}
		/>
		<div class="absolute right-0 w-[40vw] h-full">
			<div
				class="m-10 bg-slate-50 h-[90%] rounded-2xl border-2 shadow-xl border-white snap-x overflow-x-scroll flex flex-row snap-mandatory no-scrollbar"
				on:scroll={onScroll}
				bind:this={locationRef}
			>
				{#each $buildingStore as building, idx}
					<Building {building} bind:ref={locationRefs[idx]} />
				{/each}
			</div>
		</div>
	</div>
{/if}
