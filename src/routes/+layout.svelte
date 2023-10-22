<script lang="ts">
	import { onAuthStateChanged } from 'firebase/auth';
	import './app.css';
	import 'mapbox-gl/dist/mapbox-gl.css';
	import { auth, userStore } from '$lib/utils/firebase';
	import { onNavigate } from '$app/navigation';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';

	const queryClient = new QueryClient();

	onAuthStateChanged(auth, (user) => {
		userStore.set(user);
	});

	onNavigate((navigation) => {
		if (!document.startViewTransition) {
			return;
		}

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
</script>

<QueryClientProvider client={queryClient}>
	<slot />
</QueryClientProvider>
