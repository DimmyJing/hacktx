<script lang="ts">
	import { goto } from '$app/navigation';
	import Appicon from '$lib/components/appicon.svelte';
	import { baseURL } from '$lib/utils/constants';
	import { auth, userStore } from '$lib/utils/firebase';
	import { createQuery } from '@tanstack/svelte-query';
	import axios from 'axios';
	import { getIdToken, signOut } from 'firebase/auth';

	let displayName = '';
	$: if ($userStore?.displayName) displayName = $userStore.displayName;

	const query = createQuery({
		queryKey: ['profile'],
		queryFn: async () => {
			const idToken = await getIdToken(auth.currentUser!);
			return await axios.get<{
				numBuildings: number;
				collectiveOccupancyDays: number;
				predictedHomelessnessPrevented: number;
				positiveComments: string[];
			}>(baseURL + 'profile', {
				headers: {
					Authorization: 'Bearer ' + idToken
				}
			});
		}
	});

	function onLogOut() {
		goto('/');
		signOut(auth);
	}
</script>

<div class="m-14">
	<Appicon fillColor="#000" />
</div>

{#if $query.isLoading}
	<div class="flex items-center justify-center w-full h-full">
		<span class="m-14 loading loading-infinity loading-lg" />
	</div>
{:else}
	<div class="flex flex-col items-center w-full">
		<div class="flex flex-col w-full max-w-4xl">
			<h1 class="w-full text-4xl">Hi {displayName}!</h1>
			<dl class="grid grid-cols-1 gap-5 mt-5 sm:grid-cols-3">
				<div class="px-4 py-5 overflow-hidden rounded-lg shadow bg-slate-100 sm:p-6">
					<dt class="text-sm font-medium text-gray-500 truncate">Number of Buildings</dt>
					<dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
						{$query.data?.data.numBuildings}
					</dd>
				</div>
				<div class="px-4 py-5 overflow-hidden rounded-lg shadow bg-slate-100 sm:p-6">
					<dt class="text-sm font-medium text-gray-500 truncate">Collective Occupancy Days</dt>
					<dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
						{$query.data?.data.collectiveOccupancyDays}
					</dd>
				</div>
				<div class="px-4 py-5 overflow-hidden rounded-lg shadow bg-slate-100 sm:p-6">
					<dt class="text-sm font-medium text-gray-500 truncate">
						Predicted Homelessness Prevented
					</dt>
					<dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
						{$query.data?.data.predictedHomelessnessPrevented}
					</dd>
				</div>
			</dl>

			<h1 class="mt-8 mb-2 text-3xl">Feedback</h1>
			<div class="flex flex-col divide-y gap-y-2">
				{#each $query.data?.data.positiveComments ?? [] as comment}
					<span class="block pt-2 text-lg font-light">⭐ {comment}</span>
				{/each}
			</div>

			<button class="mt-16 btn btn-outline btn-error" on:click={onLogOut}>Log Out</button>
		</div>
	</div>
{/if}
