<script lang="ts">
	import { buildingStore, type building } from '$lib/utils/buildings';
	import OpenAI from 'openai';
	import type { PageData } from './$types';
	import { createMutation, createQuery } from '@tanstack/svelte-query';
	import axios, { type AxiosResponse, type InternalAxiosRequestConfig } from 'axios';
	import { auth } from '$lib/utils/firebase';
	import { getIdToken } from 'firebase/auth';
	import { onDestroy } from 'svelte';
	export let data: PageData;
	$: id = data.id;

	$: buildingVal = Number.isInteger(+id)
		? +id < $buildingStore.length
			? $buildingStore[+id]
			: undefined
		: undefined;

	const buildingQuery = createQuery({
		queryKey: ['buildings'],
		queryFn: () => axios.get<building[]>('http://localhost:8000/buildings')
	});

	$: if ($buildingQuery.data?.data) {
		buildingStore.set($buildingQuery.data.data);
	}

	const query = createQuery({
		queryKey: ['chat', id],
		queryFn: async (): Promise<
			AxiosResponse<{
				receiverAvatar: string;
				receiverName: string;
				receiverEmail: string;
				chat: { text: string; user: boolean }[];
			}>
		> => {
			if (Number.isInteger(+id)) {
				return {
					data: {
						receiverAvatar: $buildingStore[+id].image,
						receiverName: $buildingStore[+id].name,
						receiverEmail: '',
						chat: messages
					},
					status: 200,
					statusText: 'OK',
					headers: {},
					config: {} as unknown as InternalAxiosRequestConfig
				};
			}
			const token = await getIdToken(auth.currentUser!);
			return axios.get<{
				receiverAvatar: string;
				receiverName: string;
				receiverEmail: string;
				chat: { text: string; user: boolean }[];
			}>('http://localhost:8000/get_chat/' + id, {
				headers: {
					Authorization: 'Bearer ' + token
				}
			});
		},
		refetchInterval: 200
	});

	const mutation = createMutation({
		mutationFn: async (message: string) => {
			const token = await getIdToken(auth.currentUser!);
			return axios.post(
				'http://localhost:8000/send_message',
				{ uid2: id, message },
				{
					headers: {
						Authorization: 'Bearer ' + token
					}
				}
			);
		}
	});

	const openAI = new OpenAI({
		apiKey: import.meta.env.VITE_OPENAI_API_KEY,
		dangerouslyAllowBrowser: true
	});

	let useOpenAI = false;
	let systemPrompt = '';

	$: if (buildingVal) {
		useOpenAI = true;
		systemPrompt +=
			'You are the famous building ' +
			buildingVal.name +
			". You are to have an accurate and interesting conversation with the user as this building mimicing their mannerisms to the tee. Also try to make the response as humerous as possible. Here is a basic summary of the building you're playing as: " +
			buildingVal.significance;
	}

	let messageValue = '';

	let messages: {
		user: boolean;
		text: string;
	}[] = [];

	$: if ($query.data?.data) {
		messages = $query.data.data.chat;
	}

	async function getOpenAIResponse() {
		const openAIMessages = messages.map((message) => ({
			role: message.user ? ('user' as const) : ('assistant' as const),
			content: message.text
		}));
		const requestMessages = [{ role: 'system' as const, content: systemPrompt }, ...openAIMessages];
		const stream = await openAI.chat.completions.create({
			messages: requestMessages,
			model: 'gpt-4-32k',
			stream: true
		});
		messages.push({ user: false, text: '' });
		for await (const part of stream) {
			messages[messages.length - 1].text += part.choices[0].delta.content || '';
			messages = messages;
		}
	}

	$: sendMessage = () => {
		messages.push({ user: true, text: messageValue });
		messages = messages;
		messageValue = '';
		if (useOpenAI) getOpenAIResponse();
		else {
			$mutation.mutate(messages[messages.length - 1].text);
		}
	};

	$: if (messages.length > 0 && stopperRef) {
		stopperRef.scrollIntoView({
			behavior: 'smooth'
		});
	}

	onDestroy(() => {
		messages = [];
	});

	let stopperRef: HTMLDivElement;
</script>

{#if $query.isLoading && (!Number.isInteger(+id) || buildingVal === undefined)}
	<span>Loading...</span>
{:else}
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
								src={$query.data?.data.receiverAvatar ?? buildingVal?.image ?? ''}
								alt=""
							/>
						</div>
						<h3 class="ml-4 text-base font-semibold leading-6 text-gray-900">
							{$query.data?.data.receiverName ?? buildingVal?.name ?? ''}
						</h3>
					</div>
				</div>
				<div class="flex flex-shrink-0 mt-4 ml-4">
					<a
						type="button"
						class="relative inline-flex items-center px-3 py-2 ml-3 text-sm font-semibold text-gray-900 bg-white rounded-md shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
						href={'mailto:' + $query.data?.data.receiverEmail ?? ''}
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
					</a>
				</div>
			</div>
		</div>

		<div class="w-full h-[calc(100vh-185px)] max-w-3xl overflow-y-scroll no-scrollbar">
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
			<div bind:this={stopperRef} />
		</div>
		<div class="flex flex-row items-center w-full max-w-3xl">
			<input
				type="text"
				placeholder="Type here"
				class="w-full m-4 input input-bordered"
				bind:value={messageValue}
			/>
			<button class="btn btn-circle btn-outline" on:click={sendMessage}>
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
{/if}
