<script lang="ts">
	import { goto } from '$app/navigation';
	import Appicon from '$lib/components/appicon.svelte';
	import { auth, userStore } from '$lib/utils/firebase';
	import { GoogleAuthProvider, signInWithEmailAndPassword, signInWithPopup } from 'firebase/auth';

	$: if ($userStore !== null) {
		goto('/app');
	}

	let email = '';
	let password = '';

	async function signInEmail() {
		await signInWithEmailAndPassword(auth, email, password);
	}

	async function signInWithGoogle() {
		const provider = new GoogleAuthProvider();
		await signInWithPopup(auth, provider);
	}
</script>

<div class="flex flex-col justify-center min-h-full py-12 sm:px-6 lg:px-8">
	<div class="flex flex-col items-center sm:mx-auto sm:w-full sm:max-w-md">
		<Appicon fillColor="#000" />
		<h2 class="mt-6 text-2xl font-bold leading-9 tracking-tight text-center text-gray-900">
			Sign in to your account
		</h2>
	</div>

	<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
		<div class="px-6 py-12 bg-white shadow sm:rounded-lg sm:px-12">
			<form class="space-y-6" action="#" method="POST">
				<div>
					<label for="email" class="block text-sm font-medium leading-6 text-gray-900">
						Email address
					</label>
					<div class="mt-2">
						<input
							id="email"
							name="email"
							type="email"
							autocomplete="email"
							required
							class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
							bind:value={email}
						/>
					</div>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium leading-6 text-gray-900">
						Password
					</label>
					<div class="mt-2">
						<input
							id="password"
							name="password"
							type="password"
							autocomplete="current-password"
							required
							class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
							bind:value={password}
						/>
					</div>
				</div>

				<div>
					<button
						type="submit"
						class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
						on:click={signInEmail}
					>
						Sign in
					</button>
				</div>
			</form>

			<div>
				<div class="relative mt-10">
					<div class="absolute inset-0 flex items-center" aria-hidden="true">
						<div class="w-full border-t border-gray-200" />
					</div>
					<div class="relative flex justify-center text-sm font-medium leading-6">
						<span class="px-6 text-gray-900 bg-white">Or continue with</span>
					</div>
				</div>

				<div class="mt-6">
					<button
						class="flex w-full items-center justify-center gap-3 rounded-md px-3 py-1.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#24292F] border border-slate-500"
						on:click={signInWithGoogle}
					>
						<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
							<path
								d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
								fill="#4285F4"
							/>
							<path
								d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
								fill="#34A853"
							/>
							<path
								d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
								fill="#FBBC05"
							/>
							<path
								d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
								fill="#EA4335"
							/>
							<path d="M1 1h22v22H1z" fill="none" />
						</svg>
						<span class="text-sm font-semibold leading-6">Sign in with Google</span>
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
