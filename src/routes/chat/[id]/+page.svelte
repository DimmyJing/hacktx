<script lang="ts">
	import { getIdToken } from 'firebase/auth';
	import type { PageData } from './$types';
	import { userStore } from '$lib/utils/firebase';
	export let data: PageData;
	$: id = data.id;

	const avatar =
		'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80';

	let messageValue = '';

	let messages: {
		user: boolean;
		text: string;
	}[] = [
		{ user: true, text: 'hello' },
		{ user: false, text: 'hi' },
		{ user: true, text: 'hello' },
		{ user: false, text: 'hi' }
	];
</script>

<div class="flex flex-col items-center w-full h-full">
	<div class="w-full max-w-3xl px-4 py-5 mb-4 bg-white border-b border-gray-200 sm:px-6">
		<div class="flex flex-wrap items-center justify-between -mt-4 -ml-4 sm:flex-nowrap">
			<div class="flex flex-row items-center justify-center mt-4 space-x-4">
				<a class="btn btn-circle btn-outline" href="/app">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-6 h-6"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3"
						/>
					</svg>
				</a>
				<div class="flex items-center">
					<div class="flex-shrink-0">
						<img
							class="w-12 h-12 rounded-full"
							src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
							alt=""
						/>
					</div>
					<h3 class="ml-4 text-base font-semibold leading-6 text-gray-900">Tom Cook</h3>
				</div>
			</div>
			<div class="flex flex-shrink-0 mt-4 ml-4">
				<button
					type="button"
					class="relative inline-flex items-center px-3 py-2 ml-3 text-sm font-semibold text-gray-900 bg-white rounded-md shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
				>
					<svg
						class="-ml-0.5 mr-1.5 h-5 w-5 text-gray-400"
						viewBox="0 0 20 20"
						fill="currentColor"
						aria-hidden="true"
					>
						<path
							d="M3 4a2 2 0 00-2 2v1.161l8.441 4.221a1.25 1.25 0 001.118 0L19 7.162V6a2 2 0 00-2-2H3z"
						/>
						<path
							d="M19 8.839l-7.77 3.885a2.75 2.75 0 01-2.46 0L1 8.839V14a2 2 0 002 2h14a2 2 0 002-2V8.839z"
						/>
					</svg>
					<span>Email</span>
				</button>
			</div>
		</div>
	</div>

	<div class="w-full h-[calc(100vh-185px)] max-w-3xl">
		{#each messages as message}
			{#if message.user}
				<div class="chat chat-end">
					<div class="chat-bubble">{message.text}</div>
				</div>
			{:else}
				<div class="chat chat-start">
					<div class="chat-bubble">{message.text}</div>
				</div>
			{/if}
		{/each}
	</div>
	<div class="flex flex-row items-center w-full max-w-3xl">
		<input
			type="text"
			placeholder="Type here"
			class="w-full m-4 input input-bordered"
			bind:value={messageValue}
		/>
		<button class="btn btn-circle btn-outline">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="w-6 h-6"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
				/>
			</svg>
		</button>
	</div>
</div>
