<script lang="ts">
	import Peoplelist from './peoplelist.svelte';

	export let location: {
		lng: number;
		lat: number;
		name: string;
		image: string;
	};
	export let ref: HTMLElement;
</script>

<div class="min-w-[calc(40vw-5rem-4px)] snap-center" bind:this={ref}>
	<div class="relative w-full aspect-video">
		<div class="absolute w-full overflow-hidden rounded-t-2xl">
			<img
				src={location.image}
				alt={location.name}
				class="object-cover w-full aspect-video bg-gradient-to-b from-transparent to-black"
			/>
		</div>
		<div class="absolute w-full overflow-hidden rounded-t-2xl">
			<div class="from-transparent to-black/70 bg-gradient-to-b aspect-video" />
		</div>
	</div>
	<div class="relative">
		<h1 class="absolute ml-4 text-3xl text-white -top-12">{location.name}</h1>
	</div>
	<Peoplelist />
</div>
