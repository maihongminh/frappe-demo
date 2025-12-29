import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
	plugins: [vue()],
	build: {
		outDir: '../public/frontend',
		emptyOutDir: true,
		rollupOptions: {
			input: {
				main: resolve(__dirname, 'src/main.js'),
			},
			output: {
				entryFileNames: 'js/[name].js',
				chunkFileNames: 'js/[name].js',
				assetFileNames: 'assets/[name].[ext]',
			},
		},
	},
	resolve: {
		alias: {
			'@': resolve(__dirname, 'src'),
		},
	},
});

