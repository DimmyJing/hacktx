<script lang="ts">
	import { goto } from '$app/navigation';
	import Appicon from '$lib/components/appicon.svelte';
	import { auth, userStore } from '$lib/utils/firebase';
	import { signOut } from 'firebase/auth';

	let displayName = '';
	$: if ($userStore?.displayName) displayName = $userStore.displayName;

	function onLogOut() {
		goto('/');
		signOut(auth);
	}
</script>

<div class="m-14">
	<Appicon fillColor="#000" />
</div>

<div class="flex flex-col items-center w-full">
	<div class="flex flex-col w-full max-w-3xl">
		<h1 class="w-full text-4xl">Hi {displayName}!</h1>
		<dl class="grid grid-cols-1 gap-5 mt-5 sm:grid-cols-3">
			<div class="px-4 py-5 overflow-hidden rounded-lg shadow bg-slate-100 sm:p-6">
				<dt class="text-sm font-medium text-gray-500 truncate">Total Subscribers</dt>
				<dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">71,897</dd>
			</div>
			<div class="px-4 py-5 overflow-hidden rounded-lg shadow bg-slate-100 sm:p-6">
				<dt class="text-sm font-medium text-gray-500 truncate">Avg. Open Rate</dt>
				<dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">58.16%</dd>
			</div>
			<div class="px-4 py-5 overflow-hidden rounded-lg shadow bg-slate-100 sm:p-6">
				<dt class="text-sm font-medium text-gray-500 truncate">Avg. Click Rate</dt>
				<dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">24.57%</dd>
			</div>
		</dl>

		<button class="mt-4 btn btn-outline btn-error" on:click={onLogOut}>Log Out</button>
	</div>
</div>
