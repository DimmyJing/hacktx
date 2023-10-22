<script lang="ts">
	import type { building } from '$lib/utils/buildings';
	import Peoplelist from './peoplelist.svelte';

	export let building: building;
	export let ref: HTMLElement;
	export let idx: number;
</script>

<div class="min-w-[calc(40vw-5rem-4px)] snap-center" bind:this={ref}>
	<div class="relative w-full aspect-video">
		<div class="absolute w-full overflow-hidden rounded-t-2xl">
			<img
				src={building.image}
				alt={building.name}
				class="object-cover w-full aspect-video bg-gradient-to-b from-transparent to-black"
			/>
		</div>
		<div class="absolute w-full overflow-hidden rounded-t-2xl">
			<div class="from-transparent to-black/70 bg-gradient-to-b aspect-video" />
		</div>
	</div>
	<div class="relative">
		<h1 class="absolute ml-4 text-3xl text-white -top-12">{building.name}</h1>
	</div>
	<Peoplelist contributors={building.contributors} buildingIdx={idx} />
</div>
