<script lang="ts">
	export let people: {
		name: string;
		avatar: string;
		role: string;
		onlineHour: number;
		userID: string;
	}[] = [
		{
			name: 'Leslie Alexander',
			avatar:
				'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
			role: 'Co-Founder / CEO',
			onlineHour: 3,
			userID: 'HIWQLA74eGa7CpQzJ0Up9SwIQqz1'
		},
		{
			name: 'Michael Foster',
			avatar:
				'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
			role: 'Co-Founder / CTO',
			onlineHour: 3,
			userID: 'HIWQLA74eGa7CpQzJ0Up9SwIQqz1'
		},
		{
			name: 'Dries Vincent',
			avatar:
				'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
			role: 'Business Relations',
			onlineHour: 0,
			userID: 'HIWQLA74eGa7CpQzJ0Up9SwIQqz1'
		},
		{
			name: 'Lindsay Walton',
			avatar:
				'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
			role: 'Front-end Developer',
			onlineHour: 3,
			userID: 'HIWQLA74eGa7CpQzJ0Up9SwIQqz1'
		},
		{
			name: 'Courtney Henry',
			avatar:
				'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
			role: 'Designer',
			onlineHour: 3,
			userID: 'HIWQLA74eGa7CpQzJ0Up9SwIQqz1'
		},
		{
			name: 'Tom Cook',
			avatar:
				'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
			role: 'Director of Product',
			onlineHour: 0,
			userID: 'HIWQLA74eGa7CpQzJ0Up9SwIQqz1'
		}
	];

	function onClickChat(userID: string) {
		console.log(userID);
	}
</script>

<span class="ml-2 text-sm text-slate-600">CONTRIBUTORS - {people.length}</span>
<ul class="bg-white divide-y divide-gray-100 shadow-sm ring-1 ring-gray-900/5">
	{#each people as person}
		<li class="relative flex justify-between px-4 py-5 gap-x-6 hover:bg-gray-50 sm:px-6">
			<div class="flex min-w-0 gap-x-4">
				<img class="flex-none w-12 h-12 rounded-full bg-gray-50" src={person.avatar} alt="" />
				<div class="flex-auto min-w-0">
					<p class="text-sm font-semibold leading-6 text-gray-900">
						{person.name}
					</p>
					<p class="text-xs leading-6 text-gray-600">{person.role}</p>
				</div>
			</div>
			<div class="flex items-center shrink-0 gap-x-8">
				{#if person.onlineHour > 0}
					<p class="mt-1 text-xs leading-5 text-gray-500">
						Active <time>{person.onlineHour}h ago</time>
					</p>
				{:else}
					<div class="mt-1 flex items-center gap-x-1.5">
						<div class="flex-none p-1 rounded-full bg-emerald-500/20">
							<div class="h-1.5 w-1.5 rounded-full bg-emerald-500" />
						</div>
						<p class="text-xs leading-5 text-gray-500">Online</p>
					</div>
				{/if}
				<a
					type="button"
					class="mr-2 text-white rounded-full hover:text-indigo-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
					href={'/chat/' + person.userID}
				>
					<svg class="w-5 h-5" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg"
						><g id="SVGRepo_bgCarrier" stroke-width="0" /><g
							id="SVGRepo_tracerCarrier"
							stroke-linecap="round"
							stroke-linejoin="round"
						/><g id="SVGRepo_iconCarrier">
							<path
								fill-rule="evenodd"
								clip-rule="evenodd"
								d="M12.5 3L2.49999 3.00002C1.67157 3.00002 0.999999 3.67159 0.999999 4.50002V9.50002C0.999999 10.3284 1.67157 11 2.5 11H7.50002C7.63263 11 7.75981 11.0527 7.85358 11.1465L9.99999 13.2929V11.5C9.99999 11.2239 10.2239 11 10.5 11H12.5C13.3284 11 14 10.3284 14 9.50002V4.5C14 3.67157 13.3284 3 12.5 3ZM2.49999 2.00002L12.5 2C13.8807 2 15 3.11928 15 4.5V9.50002C15 10.8807 13.8807 12 12.5 12H11V14.5C11 14.7022 10.8782 14.8845 10.6913 14.9619C10.5045 15.0393 10.2894 14.9965 10.1464 14.8535L7.29292 12H2.5C1.11929 12 0 10.8807 0 9.50002V4.50002C0 3.11931 1.11928 2.00002 2.49999 2.00002Z"
								fill="#000000"
							/>
						</g></svg
					>
				</a>
			</div>
		</li>
	{/each}
</ul>
